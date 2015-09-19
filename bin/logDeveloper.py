#!/usr/bin/env python

from qore import mkdir_p
import time, sys, os
import gtk

#try:
#    env = os.environ.copy()
#    os.environ.setdefault('XAUTHORITY', '/home/qore2/.Xauthority')
#    os.environ.setdefault('DISPLAY', ':1.0')
#    #os.environ['DISPLAY'] = ':0.0'
#    #os.environ['DISPLAY'] = 'DISPLAY'
#except Exception as e:
#    print e

#os.environ['DISPLAY'] = ":0.0"

# faster alternatives: http://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows

# source: http://stackoverflow.com/questions/69645/take-a-screenshot-via-a-python-script-linux
def takeScreenshot(fname, verbose=False):

    #try:
    #    print os.environ['XAUTHORITY']
    #    print os.environ['DISPLAY']
    #    print os.environ['USER']
    #except Exception as e:
    #    print e

    try:
        #w = gtk.gdk.get_default_root_window()
        w = gtk.gdk.get_default_root_window().get_screen().get_active_window()
        sz = w.get_size()
        if verbose == True: print "The size of the window is %d x %d" % sz
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
        pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
        if (pb != None):
            pb.save(fname,"png")
            print "Screenshot saved to "+fname
        else:
            print "Unable to get the screenshot."
    except Exception as e:
        print e
        print "Unable to get the screenshot."
        
def projectLog(projectName):
    try:
        ts = time.time()
        developer = os.environ['USER']
        print developer
        developer = developer.lower().replace(' ', '_')
        hdir = '/mldev/screenshots/developerLogs/screen/{0}'.format(developer)
        mkdir_p(hdir)
        fname = "{0}/{1}-screenshot-{3}-{2}.png".format(hdir, projectName, int(ts), developer)
        #time.strptime('%Y',)
        print '{1}:: screenshot saved to: {0}'.format(fname, int(ts))
        takeScreenshot(fname)
    except Exception as e:
        print e
projectLog('liquid')
