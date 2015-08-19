
import digitalocean
import numpy as n
class HPC:
    
    def __init__(self):
        
        self.token = "fb13f87e074de9bcfba1fca4844b4823a85272d7902418a5776445bcdea250b9"
        self.pkey  = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCoa61+j5xyI1c0cfRhmx1ggEzScbzs2VBLvEsbNB5M1rNqWqVT/Wou7XnEWZzijcNuuZtYDZZRegCRfN4VH+DNpT4uaykShYp1XNRuDK7fXttDbxhg2XIrfBoW6lvTt1K2xWQP/dOMg0DjRmjRbGL3OQpcyaOofmE7+0WMDqySa/MhYk7AJhgBVYoBh43W0f4Jv+JAaxz4RTxiHGwIIYDHLDI67nupWXgzFOvj29LNh3/qtfJAQUhdBRfcuOpZyglBxYlMw5o/7euSe+oYhmdWM11g/0MOOYonkOl1Yg3/E5AACV7P9y5db7aVttAfnAD6XXIqUj74u3PHJ8Nji5dB kiizaa@gmail.com'
        
        self.manager = digitalocean.Manager(token=self.token)
        
    def getImages(self):
        
        #im = self.manager.get_all_images()
        #im = self.manager.get_images()
        im = self.manager.get_my_images()

        #print
        #print 'images:'
        ims = {}
        for i in im:
            ims[i.id] = i#.name
        return ims

    def getLastImage(self):
        
        ims = self.getImages().keys()
        return n.max(ims)
    
    def getNodes(self, quiet=False):
        
        #print
        #print 'nodes:'
        my_droplets = self.manager.get_all_droplets()
        droplets = []
        for droplet in my_droplets:
            droplets.append(droplet)
            if quiet == False:
                print droplet.id
                print 'ssh -oStrictHostKeyChecking=no root@{0}'.format(droplet.ip_address)
                print 'ipython notebook --ip={0}'.format(droplet.ip_address)
        return droplets

        #    #droplet.shutdown()
    
    def createNode(self):
        
        key = digitalocean.SSHKey(token=self.token)
        dkey = key.load_by_pub_key(self.pkey)

        droplet = digitalocean.Droplet(token=self.token,
                                       name='liquid-rc07',
                                       #region='nyc2', # New York 2
                                       region=self.getImages()[self.getLastImage()].regions[0],
                                       #image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
                                       image=self.getLastImage(),
                                       size_slug='512mb',  # 512MB
                                       backups=True, ssh_keys=[dkey])
        droplet.create()
    
    def makeNewSnapshot(self, droplet):
        images = self.getImages()
        lastImage = images[self.getLastImage()].name.split(' ')[0]
        str1 = lastImage.split('rc')[0]
        str2 = '%02.f' % (int(lastImage.split('rc')[1])+1)
        print type(str1)
        print type(str2)
        newSnapshotName = '{0}rc{1}'.format(str1, str2)
        try:
            droplet.take_snapshot(newSnapshotName)
        except:
            ans = raw_input('turn off droplet {1}({0})? y/n: '.format(droplet.id, droplet.name))
            ''
            droplet.power_off()
            droplet.take_snapshot(newSnapshotName)
    
