#!/usr/bin/env python

class HPC:
    
    def __init__(self):
        self.qd = qd
        self.qd._getMethod()
        
        self.token = "fb13f87e074de9bcfba1fca4844b4823a85272d7902418a5776445bcdea250b9"
        self.pkey  = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCoa61+j5xyI1c0cfRhmx1ggEzScbzs2VBLvEsbNB5M1rNqWqVT/Wou7XnEWZzijcNuuZtYDZZRegCRfN4VH+DNpT4uaykShYp1XNRuDK7fXttDbxhg2XIrfBoW6lvTt1K2xWQP/dOMg0DjRmjRbGL3OQpcyaOofmE7+0WMDqySa/MhYk7AJhgBVYoBh43W0f4Jv+JAaxz4RTxiHGwIIYDHLDI67nupWXgzFOvj29LNh3/qtfJAQUhdBRfcuOpZyglBxYlMw5o/7euSe+oYhmdWM11g/0MOOYonkOl1Yg3/E5AACV7P9y5db7aVttAfnAD6XXIqUj74u3PHJ8Nji5dB kiizaa@gmail.com'
        self.key_vultr = ''
        
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
    
    def printNodeManifest(self, node_id, ip_address, label, location, date_created, passwd=''):
        print 'id:{0}'.format(node_id)
        print 'label:{0}'.format(label)
        print 'location:{0}'.format(location)
        print 'date_created:{0}'.format(date_created)
        print 'passwd: {0}'.format(passwd)
        print '    ping {0}'.format(ip_address)
        print '    ssh -L 3310:127.0.0.1:27017 -oStrictHostKeyChecking=no root@{0}'.format(ip_address)
        print ''
        print '  X11 Forwarding via SSH@{0}'.format(ip_address)
        print '    ssh -X -L 3310:127.0.0.1:27017 -oStrictHostKeyChecking=no root@{0}'.format(ip_address)
        print '    ipython notebook --ip={0}'.format(ip_address)
        print '    http://{0}:5000'.format(ip_address)
        print '    rsync -av /mldev/bin/datafeeds/config.csv root@{0}:/home/qore/mldev/bin/datafeeds/config.csv'.format(ip_address)
        print '    rsync -avP --partial root@{0}:/home/qore/mldev/bin/data/db-archive/ /mldev/bin/data/db-archive/'.format(ip_address)
        print '    rdesktop -g 100% -u qore -p - {0}'.format(ip_address)
        print 
    
    def getNodes(self, quiet=False):
        self.qd._getMethod()
        
        #print
        #print 'nodes:'
        my_droplets = self.manager.get_all_droplets()
        droplets = {}
        
        print '=== DigitalOcean ====='
        for droplet in my_droplets:
            print '--------'
            droplets[droplet.id] = droplet
            #droplets.append(droplet)
            #print droplets
            #print dir(droplet)
            if quiet == False:
                self.printNodeManifest(droplet.id, droplet.ip_address, droplet.name, droplet.region['name'], droplet.created_at)
        
        print '=== VULTR ====='
        v = Vultr(self.key_vultr)
        res = v.server_list()
        #print p.DataFrame(res)
        for i in res:
            print '--------'
            #print res[i]
            if quiet == False:
                self.printNodeManifest(i, res[i]['main_ip'], res[i]['label'], res[i]['location'], res[i]['date_created'], passwd=res[i]['default_password'])

        return droplets

        #    #droplet.shutdown()
    
    def createNode(self, provider):
        self.qd._getMethod()
        
        #provider = raw_input('Prepping node..  ..which provider? (d=DigitalOcean, v=Vultr): ')
 
        if provider == 'd':
            key = digitalocean.SSHKey(token=self.token)
            dkey = key.load_by_pub_key(self.pkey)
            
            nextSnapshotname = self.createNextSnapshotname()
            lastImage        = self.getLastImage()
            images           = self.getImages(verbose=False)
            
            droplet = digitalocean.Droplet(token=self.token,
                                           name=nextSnapshotname, #'liquid-rc07',
                                           #region='nyc2', # New York 2
                                           region=images[lastImage].regions[0],
                                           #image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
                                           image=lastImage,
                                           size_slug='512mb',  # 512MB
                                           #size_slug='1gb',  # 512MB
                                           backups=True, ssh_keys=[dkey])
            droplet.create()

        if provider == 'v':
            v = Vultr(self.key_vultr)
            res = self.plans()
            print res.ix[['29', '94'], :].transpose()
            #v.server_create(DCID=1, VPSPLANID=94, OSID=191, SCRIPTID=12633, SSHKEYID='5674534d396cf', label='liquid-compute-rc1')
            v.server_create(1, 94, 191, SCRIPTID=12633, SSHKEYID='5674534d396cf', label='liquid-compute-rc1')
            #v.server_create({'DCID':1, 'VPSPLANID':94, 'OSID':191, 'SCRIPTID':12633, 'SSHKEYID':'5674534d396cf', 'label':'liquid-compute-rc1'})
    
    def regions(self):
            v = Vultr(self.key_vultr)
            res = v.regions_list()
            df = p.DataFrame(res).transpose()
            df = df.convert_objects(convert_numeric=True)
            df = df.set_index('DCID')
            print df.sort()
        
    def plans(self):
            v = Vultr(self.key_vultr)
            res = v.plans_list()
            df = p.DataFrame(res).transpose()
            df = df.convert_objects(convert_numeric=True)
            df['price_per_hour'] = df.ix[:, 'price_per_month'] / 24 / 30
            return df.sort(['ram','vcpu_count'], ascending=False)
        
    def os(self):
            v = Vultr(self.key_vultr)
            res = v.os_list()
            print p.DataFrame(res).transpose()
        
    def startupScripts(self):
            v = Vultr(self.key_vultr)
            res = v.startupscript_list()
            print p.DataFrame(res)#.transpose()
        
    def sshkeys(self):
            v = Vultr(self.key_vultr)
            res = v.sshkey_list()
            print p.DataFrame(res)#.transpose()
        
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
        
        print '=== DigitalOcean ====='
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
                
        print '=== VULTR ====='
        v = Vultr(self.key_vultr)
        res = v.server_list()
        #print p.DataFrame(res)
        for i in res:
            print '--------'
            
            #ans = raw_input('destroy droplet {0}[{1}:{2}]? y/n: '.format(droplet.id, droplet.name, droplet.ip_address))
            #print res[i]
            #print p.DataFrame([res[i]]).transpose()
            #if quiet == False:
            self.printNodeManifest(i, res[i]['main_ip'], res[i]['label'], res[i]['location'], res[i]['date_created'], passwd=res[i]['default_password'])
            ans = raw_input('destroy vultr node {0}[{1}:{2}]? y/n: '.format(i, res[i]['label'], res[i]['main_ip']))
            if ans == 'y':
                v.server_destroy(i)
                

    def getLastImageName(self):
        self.qd._getMethod()
        
        lastImage = self.getImages()[self.getLastImage()]
        return lastImage.name

    def createNextSnapshotname(self):
        self.qd._getMethod()
        
        #print lastImage.created_at
        #print lastImage.name
        #lastImage = self.getImages(verbose=True)[self.getLastImage()]
        lastImage = self.getImages(verbose=True)[13417249]
        lim = lastImage.name.split('rc')
        #print lim
        weq = (int(lim[1].split(' ')[0])+1)
        lim = '{0}{1}{2}'.format(lim[0], 'rc', '%02d' % weq)
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

    import argparse
    # source: https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser()
    
    #        if sys.argv[1] == 'on':
    #            c.createNode()
    parser.add_argument("-on", help="d=DigitalOcean, v=Vultr")
    #        if sys.argv[1] == 'nodes':
    #            # running nodes
    #            res = c.getNodes()
    parser.add_argument("-n", "-nodes", "--nodes", help="c.getNodes()", action="store_true")
    ##        if sys.argv[1] == 'images':
    #            c.getImages()
    parser.add_argument("-i", "-images", "--images", help="c.getImages()", action="store_true")
    #        if sys.argv[1] == 'snapshot':
    #            print c.snapshotAllDroplets()
    parser.add_argument("-s", "-snapshot", "--snapshot", help="c.snapshotAllDroplets()", action="store_true")
    #        if sys.argv[1] == 'destroy':
    #            print c.destroyAllDroplets()
    parser.add_argument("-d", "-destroy", "--destroy", help="c.destroyAllDroplets()", action="store_true")
    #        if sys.argv[1] == 'regions':
    #            print c.regions()
    parser.add_argument("-r", "-regions", "--regions", help="c.regions()", action="store_true")
    parser.add_argument("-p", "-plans",   "--plans",   help="c.plans()",   action="store_true")
    parser.add_argument("-os",   "--os",   help="c.os()",   action="store_true")
    parser.add_argument("-ss",   "--startup",   help="c.startupScripts()",   action="store_true")
    parser.add_argument("-sk",   "--sshkeys",   help="c.sshkeys()",   action="store_true")

    #print 'usage: <hpc.py on | nodes | images | snapshot | destroy | regions>'

    args = parser.parse_args()
    
    import digitalocean
    from vultr.vultr import Vultr
    import numpy as n
    import pandas as p
    import time
    from qore import QoreDebug
    
    qd = QoreDebug()
    qd.off()
    qd.stackTraceOff()

    c = HPC()

    if args.on:
        c.createNode(args.on)
    if args.nodes:
        c.getNodes()
    if args.images:
        c.getImages()
    if args.snapshot:
        c.snapshotAllDroplets()
    if args.destroy:
        c.destroyAllDroplets()
    if args.regions:
        c.regions()
    if args.plans:
        print c.plans()
    if args.os:
        c.os()
    if args.startup:
        c.startupScripts()
    if args.sshkeys:
        c.sshkeys()
