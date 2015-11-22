#!/usr/bin/env python

import digitalocean
import numpy as n
import time

from qore import QoreDebug

qd = QoreDebug()
qd.off()
qd.stackTraceOff()

class HPC:
    
    def __init__(self):
        self.qd = qd
        self.qd._getMethod()
        
        self.token = "fb13f87e074de9bcfba1fca4844b4823a85272d7902418a5776445bcdea250b9"
        self.pkey  = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCoa61+j5xyI1c0cfRhmx1ggEzScbzs2VBLvEsbNB5M1rNqWqVT/Wou7XnEWZzijcNuuZtYDZZRegCRfN4VH+DNpT4uaykShYp1XNRuDK7fXttDbxhg2XIrfBoW6lvTt1K2xWQP/dOMg0DjRmjRbGL3OQpcyaOofmE7+0WMDqySa/MhYk7AJhgBVYoBh43W0f4Jv+JAaxz4RTxiHGwIIYDHLDI67nupWXgzFOvj29LNh3/qtfJAQUhdBRfcuOpZyglBxYlMw5o/7euSe+oYhmdWM11g/0MOOYonkOl1Yg3/E5AACV7P9y5db7aVttAfnAD6XXIqUj74u3PHJ8Nji5dB kiizaa@gmail.com'
        
        self.manager = digitalocean.Manager(token=self.token)
        
    def getImages(self, verbose=True):
        self.qd._getMethod()
        
        #im = self.manager.get_all_images()
        #im = self.manager.get_images()
        im = self.manager.get_my_images()

        #print
        #print 'images:'
        ims = {}
        for i in im:
            ims[i.id] = i#.name
        if verbose == True:
            for img in ims:
                print '{0} {1} {2}'.format(ims[img].id, ims[img].name.split(' ')[0], ims[img].created_at)
            print
        return ims

    def getLastImage(self):
        self.qd._getMethod()
        
        images = self.getImages(verbose=False)
        #print images
        ims = images.keys()
        return n.max(ims)
    
    def getNodes(self, quiet=False):
        self.qd._getMethod()
        
        #print
        #print 'nodes:'
        my_droplets = self.manager.get_all_droplets()
        droplets = {}
        for droplet in my_droplets:
            droplets[droplet.id] = droplet
            #droplets.append(droplet)
            if quiet == False:
                print droplet.id
                print '    ping {0}'.format(droplet.ip_address)
                print '    ssh -oStrictHostKeyChecking=no root@{0}'.format(droplet.ip_address)
                print ''
                print '  X11 Forwarding via SSH@{0}'.format(droplet.ip_address)
                print '    ssh -X -oStrictHostKeyChecking=no root@{0}'.format(droplet.ip_address)
                print '    ipython notebook --ip={0}'.format(droplet.ip_address)
                print '    ping {0}'.format(droplet.ip_address)
                print '    http://{0}:5000'.format(droplet.ip_address)
                print '    rsync -av /mldev/bin/datafeeds/config.csv root@{0}:/home/qore/mldev/bin/datafeeds/config.csv'.format(droplet.ip_address)
                print '    rsync -avPn root@{0}:/home/qore/mldev/bin/data/db-archive/ /mldev/bin/data/db-archive/'.format(droplet.ip_address)
                print '    rdesktop -u qore -p - {0}'.format(droplet.ip_address)
        return droplets

        #    #droplet.shutdown()
    
    def createNode(self, name=None):
        self.qd._getMethod()
        
        key = digitalocean.SSHKey(token=self.token)
        dkey = key.load_by_pub_key(self.pkey)
        
        if name != None:
            nextSnapshotname = name
        else:
            nextSnapshotname = self.createNextSnapshotname()
            
        lastImage        = self.getLastImage()
        images           = self.getImages(verbose=False)
        
        if name == 'h2o-worker':
            image = 'h2o-worker-1448226543'
        else:
            image = lastImage

        droplet = digitalocean.Droplet(token=self.token,
                                       name=nextSnapshotname, #'liquid-rc07',
                                       #region='nyc2', # New York 2
                                       region=images[lastImage].regions[0],
                                       #image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
                                       image=image,
                                       size_slug='512mb',  # 512MB
                                       #size_slug='1gb',  # 512MB
                                       backups=True, ssh_keys=[dkey])
        droplet.create()
    
    def makeNewSnapshot(self, droplet):
        self.qd._getMethod()
        
        newSnapshotName = self.createNextSnapshotname()
        try:
            droplet.take_snapshot(newSnapshotName)
        except:
            ans = raw_input('turn off droplet {1}({0})? y/n: '.format(droplet.id, droplet.name))
            ''
            droplet.power_off()
            droplet.take_snapshot(newSnapshotName)
    

    
    def snapshotAllDroplets(self):
        self.qd._getMethod()
        
        # make snapshot of droplets
        wait = 5
        
        droplets = self.getNodes(quiet=True)
        for id in droplets:
            
            droplet = droplets[id]
            ans = raw_input('turn off droplet {1}({0})? y/n: '.format(droplet.id, droplet.name))
            #ans = 'y'
            if ans == 'y':
                while True:
                    try:
                        print 
                        print 'events:'
                        for i in droplet.get_events():
                            print i
                        print
                        print 'attempting snapshot({0}) '.format(droplet.id)
                        #droplet.power_off()
                        self.makeNewSnapshot(droplet)
                        print 'waiting {0} secs'.format(wait)
                        time.sleep(5)
                        clear_output()
                    except Exception as e:
                        print e
                        break
            else:
                print 'nothing done'

    def destroyAllDroplets(self):
        self.qd._getMethod()
        
        # destroy droplets
        wait = 5
        
        droplets = self.getNodes(quiet=True)
        for id in droplets:
            
            droplet = droplets[id]
            ans = raw_input('destroy droplet {0}[{1}:{2}]? y/n: '.format(droplet.id, droplet.name, droplet.ip_address))
            #ans = 'y'
            if ans == 'y':
                while True:
                    try:
                        print 
                        print 'events:'
                        for i in droplet.get_events():
                            print i
                        print
                        droplet.destroy()
                        time.sleep(5)
                        clear_output()
                    except Exception as e:
                        print e
                        break
            else:
                print 'nothing done'

    def getLastImageName(self):
        self.qd._getMethod()
        
        lastImage = self.getImages()[self.getLastImage()]
        return lastImage.name

    def createNextSnapshotname(self):
        self.qd._getMethod()
        
        lastImage = self.getImages(verbose=False)[self.getLastImage()]
        #print lastImage.created_at
        #print lastImage.name
        lim = lastImage.name.split('rc')
        #print lim
        lim = '{0}{1}{2}'.format(lim[0], 'rc', '%02d' % (int(lim[1].split(' ')[0])+1))
        #print lim
        return lim

    def createNextSnapshotname2(self):
        self.qd._getMethod()
        
        images = self.getImages()
        lastImage = images[self.getLastImage()].name.split(' ')[0]
        str1 = lastImage.split('rc')[0]
        str2 = '%02.f' % (int(lastImage.split('rc')[1])+1)
        #print type(str1)
        #print type(str2)
        return '{0}rc{1}'.format(str1, str2)

if __name__ == "__main__":
    import sys
    import threading
    
    c = HPC()

    def threadCreateNode():
        c = HPC()
        #nextSnapshotname = self.createNextSnapshotname()
        c.createNode(name='h2o-worker')
    
    try:
        if sys.argv[1] == 'on':
            if sys.argv[2] == 'h2o-worker':
                thr = []
                num = int(sys.argv[3])
                for i in xrange(num):
                    print 'starting {0} h2o-workers: h2o-worker-{1}'.format(num, i)
                    thr.append(threading.Thread(target=threadCreateNode, args=[]))
                    thr[i].daemon = False
                    thr[i].start()
            if sys.argv[2] == 'liquid':
                c.createNode()
        if sys.argv[1] == 'nodes':
            # running nodes
            res = c.getNodes()
        if sys.argv[1] == 'images':
            c.getImages()
        if sys.argv[1] == 'snapshot':
            print c.snapshotAllDroplets()
        if sys.argv[1] == 'destroy':
            print c.destroyAllDroplets()
    except Exception as e:
        print 'usage: <hpc.py on [liquid|(h2o-master|h2o-worker <numberOfNodes>)] | nodes | images | snapshot | destroy>'
        print e
