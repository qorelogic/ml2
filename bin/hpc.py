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
    
    def printNodeManifest(self, node_id, ip_address, label, location, date_created, passwd='', maskPasswd=True, ptype='verbose'):
        
        getPasswd = lambda x: passwd if (maskPasswd==False) else '---'

        di = {
            'node_id':       node_id,
            'ip_address':    ip_address,
            'label':         label,
            'location':      location,
            'date_created':  date_created,
            #'passwd':        passwd,
            'passwd':        getPasswd(True),

            'ping-to':       'ping {0}'.format(ip_address),
            'ssh-to':        'ssh -X -L 3310:127.0.0.1:27017 -oStrictHostKeyChecking=no root@{0}'.format(ip_address),
            'x11-to':        'X11 Forwarding via SSH@{0}'.format(ip_address),
            'ipynb':         'ipython notebook --ip={0}'.format(ip_address),
            'na1':           'http://{0}:5000'.format(ip_address),
            'config.csv':    'rsync -av /mldev/bin/datafeeds/config.csv root@{0}:/home/qore/mldev/bin/datafeeds/config.csv'.format(ip_address),
            'instruments':   'rsync -av /mldev/bin/data/oanda/cache/ root@{0}:/home/qore/mldev/bin/data/oanda/cache/'.format(ip_address),
            'db-archive':    'rsync -avP --partial root@{0}:/home/qore/mldev/bin/data/db-archive/ /mldev/bin/data/db-archive/'.format(ip_address),
            'rdesktop':      'rdesktop -g 100% -u qore -p - {0}'.format(ip_address),
            'zmq-client':    'python zmq-client.py %s:5555 avg' % ip_address,
        }
        #print ' '.join(di.keys())

        if ptype == 'list':
            df = p.DataFrame(di, index=[0]).set_index('node_id')#.transpose()
            return df
        else:
            print 'id:{0}'.format(node_id)
            print 'label:{0}'.format(label)
            print 'location:{0}'.format(location)
            print 'date_created:{0}'.format(date_created)
            print 'passwd: {0}'.format(getPasswd(True))
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
        
    def getNodes(self, quiet=False, ptype = 'list'):
        self.qd._getMethod()
        
        ch = 'label date_created ssh-to passwd ping-to rdesktop node_id ipynb ip_address id x11-to config.csv instruments na1 location db-archive zmq-client'
        
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
                self.printNodeManifest(droplet.id, droplet.ip_address, droplet.name, droplet.region['name'], droplet.created_at, ptype=ptype)
        
        print '=== VULTR ====='
        v = Vultr(self.key_vultr)
        res = v.server_list()
        #print p.DataFrame(res)
        df = p.DataFrame()
        for i in res:
            print '--------'
            #print res[i]
            if quiet == False:
                dfi = self.printNodeManifest(i, res[i]['main_ip'], res[i]['label'], res[i]['location'], res[i]['date_created'], passwd=res[i]['default_password'], ptype=ptype)
                if ptype == 'list':
                    df = df.combine_first(dfi)
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000, 'display.max_colwidth', 1000):
            print df.ix[:, ch.split(' ')].sort_values(by='date_created')#.transpose()

        return droplets

        #    #droplet.shutdown()
    
    def h2oFlatfile(self, quiet=False, ptype='list'):
        self.qd._getMethod()
        
        fname = '/tmp/ql-h2o-flatfile.txt'

        my_droplets = self.manager.get_all_droplets()
        droplets = {}
        
        """
        print '=== DigitalOcean ====='
        for droplet in my_droplets:
            print '--------'
            droplets[droplet.id] = droplet
            if quiet == False:
                self.printNodeManifest(droplet.id, droplet.ip_address, droplet.name, droplet.region['name'], droplet.created_at, ptype=ptype)
        """
        
        #print '=== VULTR ====='
        v = Vultr(self.key_vultr)
        res = v.server_list()
        df = p.DataFrame()
        li = []
        for i in res:
            if quiet == False:
                li.append(res[i]['main_ip'])
                dfi = p.DataFrame([res[i]['main_ip']], index=[i], columns=['ip'])
                if ptype == 'list':
                    df = df.combine_first(dfi)
        df['port'] = ['54321']*len(df.index)
        #print df
        #df.to_csv(fname)
        #df = p.read_csv(fname)
        #df = df.set_index('Unnamed: 0')
        li = list(df.get_values()[:,0])            
        ips = '\n'.join(map(lambda x: x+':54321', li))
        #print ips
        fp = open(fname, 'w')
        fp.write(ips)
        fp.close()
        
        for i in res:
            h2o_ip = res[i]['main_ip']
            try:
                #if h2o_ip != getIpAddr():
                import os
                cmd = "rsync -avz %s root@%s:%s" % (fname, h2o_ip, fname)
                print 'Deploying dataset to h2o cluster @ %s' % h2o_ip
                print cmd
                print os.system(cmd)
            except Exception as e:
                print e
    
    def createNode(self, provider, region=False, num=1, verbose=False):
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
            #p.set_option('display.width',       1000000)
            #p.set_option('display.max_rows',    8000)
            #p.set_option('display.max_columns', 8000)

            if not region:
                print
                print '\terror: requires -r or --region argument'
                print
                sys.exit()
            ca = c.costanalysis(region, sortby='vcpu_count ram disk bandwidth_gb', silent=True)

            import hashlib as hl
            def createNode(region, group=''):
                vpsplanid  = ca.index[0]
                regions    = c.regions()
                plans      = c.plans()
                os_type    = 164 # snapshot
                #os_type    = 191 # ubuntu
                scriptid   = 12633
                snapshotid = '71056b3453c4c'
                sshkeyid   = '5674534d396cf'
                hpad       = hl.md5(str(time.time())).hexdigest()[0:10]
                label      = 'liquid-compute-[%s]-rc2.%s' % (group, hpad)
                
                with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
                    print regions
                    print 'vpsplanid: %s' % vpsplanid
                    print plans.ix[vpsplanid, :]
                    
                if region:
                    
                    if os_type == 191:
                        # load ubuntu
                        try:
                            v.server_create(region, vpsplanid, os_type, scriptid=scriptid, sshkeyid=sshkeyid, label=label)
                        except Exception as e:
                            print e
                    
                    if os_type == 164:
                        # load snapshot
                        try:
                            v.server_create(region, vpsplanid, os_type, snapshotid=snapshotid, sshkeyid=sshkeyid, label=label)
                            ''
                        except Exception as e:
                            print e
            
            if not num: num = 1
            else:       num = int(num)
            # map
            ts = []
            import threading, time
            #print 'num: %s[%s]' % (num, type(num))
            for i in xrange(num):
                ts.append(threading.Thread(target=createNode, args=(region, 'cluster-01')))
                ts[i].daemon = False
                ts[i].start()
                # vultr has a 1 sec/node limit
                time.sleep(1.1)
            #for i in xrange(num):
            #    createNode(region, 'cluster-01')
            
    def connect(self):

        import subprocess, os
        
        #print '=== VULTR ====='
        v = Vultr(self.key_vultr)
        res = v.server_list()
        df = p.DataFrame()
        for i in res:
            dfi = p.DataFrame([res[i]['main_ip']], index=[i], columns=['ip'])
            df = df.combine_first(dfi)
        hosts = list(df['ip'].get_values())
        # source: https://exyr.org/2011/gnome-terminal-tabs/
        #command = 'ls -l'
        terminal = ['gnome-terminal']
        for host  in hosts:
            terminal.extend(['--tab', '-e', '''
                bash -c '
                    #ssh -X -L 3310:127.0.0.1:27017 -oStrictHostKeyChecking=no root@%(host)s
                    ssh -X -oStrictHostKeyChecking=no root@%(host)s
                    #read
                '
            ''' % locals()])
        os.environ['NO_AT_BRIDGE'] = "1"
        subprocess.call(terminal)
    
    def regions(self):
            v = Vultr(self.key_vultr)
            res = v.regions_list()
            df = p.DataFrame(res).transpose()
            df = df.convert_objects(convert_numeric=True)
            df = df.set_index('DCID')
            return df.sort_index().ix[:, 'name'.split()]
        
    def plans(self):
            v = Vultr(self.key_vultr)
            res = v.plans_list()
            df = p.DataFrame(res).transpose()
            df = df.convert_objects(convert_numeric=True)
            df['price_per_hour'] = df.ix[:, 'price_per_month'] / 24 / 30
            return df.sort_values(by=['ram','vcpu_count'], ascending=False)
        
    def os(self):
            v = Vultr(self.key_vultr)
            res = v.os_list()
            return p.DataFrame(res).transpose()
        
    def startupScripts(self):
            v = Vultr(self.key_vultr)
            res = v.startupscript_list()
            return p.DataFrame(res)#.transpose()
        
    def sshkeys(self):
            v = Vultr(self.key_vultr)
            res = v.sshkey_list()
            return p.DataFrame(res)#.transpose()

    def snapshots(self):
            v = Vultr(self.key_vultr)
            res = v.snapshot_list()
            return p.DataFrame(res)#.transpose()
            
    def snapshotcreate(self, subid):
            v = Vultr(self.key_vultr)
            res = v.snapshot_create(subid)
            print res
        
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
                try:
                    v.server_destroy(i)
                except Exception as e:
                    print e
                
    def rebootAllNodes(self):
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
                        #droplet.destroy()
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
            ans = raw_input('reboot vultr node {0}[{1}:{2}]? y/n: '.format(i, res[i]['label'], res[i]['main_ip']))
            if ans == 'y':
                try:
                    v.server_reboot(i)
                except Exception as e:
                    print e

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

    def costanalysis(self, regionid, sortby='vcpu_count ram disk bandwidth_gb', silent=False):
        import matplotlib.pylab as plt
        from qoreliquid import normalizeme
        
        if not regionid:
            print
            print '\terror: requires -r or --region argument'
            print
            sys.exit()
        #print 'regionid: %s' % regionid
        
        lowCost = {
             'bandwidth':'',
             'disk':'',
             'ram':'',
             'vcpu':'',
        }
         
        sortby = sortby.split(' ')
        
        v = Vultr(self.key_vultr)
        res = v.plans_list()
        df = p.DataFrame(res).transpose()
        df = df.convert_objects(convert_numeric=True)
        df['price_per_hour'] = df.ix[:, 'price_per_month'] / 24 / 30
        res0 = df.sort_values(by=['ram','vcpu_count'], ascending=False)
        
        columns = 'bandwidth bandwidth_gb disk price_per_month ram vcpu_count price_per_hour'
        a = res0.ix[0, columns.split(' ')]
        b = res0.ix[:, columns.split(' ')]
        res = a / b
        #res = b
        #plt.plot(res)
        #res = normalizeme(res)
        #res = sigmoidme(res)
        res = res.convert_objects(convert_numeric=True)
        c = n.array(res, dtype=float).T / n.array(res.ix[:,'price_per_hour'], dtype=float)
        c = (res.transpose() / res.ix[:,'price_per_hour']).transpose()

        sortbytxt = ', '.join(sortby)
        title = 'sortby: %s' % (sortbytxt)
        
        #p.set_option('max_colwidth', 80)
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):

            b['available_locations']   = res0.ix[:, 'available_locations']
            b['price_per_hour']        = res0.ix[:, 'price_per_hour']
            #print
            #print title
            #print b.sort_values(by=sortby)            
            
            res['available_locations']   = res0.ix[:, 'available_locations']
            res['price_per_hour']        = res0.ix[:, 'price_per_hour']
            #print
            #print title
            #print res.sort_values(by=sortby)
            
            c['available_locations']   = res0.ix[:, 'available_locations']
            c['price_per_hour']        = res0.ix[:, 'price_per_hour']
            #c['available_locations'] = map(lambda x: x.index(1), c['available_locations'])
            for i in xrange(len(c['available_locations'])):
                try:    c.ix[i, 'available_locations'] = c['available_locations'][i].index(int(regionid))
                except: c.ix[i, 'available_locations'] = -2
            c = c[c['available_locations'] > -1]
            c = c.sort_values(by=sortby)
            if silent == False:
                print
                print title
                print c

                c.plot()
                plt.title(title)
                plt.show()
                #res.plot()
                #plt.show()            
        return c

if __name__ == "__main__":
    import sys

    import argparse
    # source: https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser()
    
    #        if sys.argv[1] == 'on':
    #            c.createNode()
    parser.add_argument("-on", help="d=DigitalOcean, v=Vultr")
    parser.add_argument("-rb", help="reboot nodes")
    parser.add_argument("-c", '--connect', help="connect, v=Vultr", action="store_true")
    parser.add_argument("-n", "-num", "--num", help="c.getNodes()")
    #        if sys.argv[1] == 'nodes':
    #            # running nodes
    #            res = c.getNodes()
    parser.add_argument("-ln", "-nodes", "--nodes", help="c.getNodes()", action="store_true")
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
    parser.add_argument("-lr", "-regions", "--regions", help="c.regions()", action="store_true")
    parser.add_argument("-r",  "-region",  "--region",  help="set the region")
    parser.add_argument("-lp", "-plans",   "--plans",   help="c.plans()",   action="store_true")
    parser.add_argument("-os",   "--os",   help="c.os()",   action="store_true")
    parser.add_argument("-ss",   "--startup",   help="c.startupScripts()",   action="store_true")
    parser.add_argument("-sk",   "--sshkeys",   help="c.sshkeys()",   action="store_true")
    parser.add_argument("-sn",   "--snapshots",   help="c.snapshots()", action="store_true")
    parser.add_argument("-snc",   "--snapshotcreate",   help="subid,description")
    #parser.add_argument("--subid",   help="subid,description", action="store_true")
    #parser.add_argument("--description",   help="subid,description", action="store_true")

    parser.add_argument("-ca", "--costanalysis",  help="cost analysis",   action="store_true")
    
    parser.add_argument("-fl", "--h2oflatfile",  help="h2oFlatfile",   action="store_true")

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
        c.createNode(args.on, region=args.region, num=args.num)
    if args.rb:
        c.rebootAllNodes()
    if args.connect:
        c.connect()
    if args.nodes:
        c.getNodes()
    if args.h2oflatfile:
        c.h2oFlatfile()
    if args.images:
        c.getImages()
    if args.snapshot:
        c.snapshotAllDroplets()
    if args.destroy:
        c.destroyAllDroplets()
    if args.regions:
        print c.regions()
    if args.plans:
        with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
            print c.plans()
    if args.os:
        print c.os()
    if args.startup:
        print c.startupScripts()
    if args.sshkeys:
        print c.sshkeys()
    if args.snapshots:
        print c.snapshots()
    if args.snapshotcreate:
        c.snapshotcreate(args.snapshotcreate)
    if args.costanalysis:
        c.costanalysis(args.region, sortby='vcpu_count ram disk bandwidth_gb')
