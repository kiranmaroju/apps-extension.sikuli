
''' Author: David Clarke
    Contributors: David Clarke, Mohamed Dabbagh
'''

import os
import subprocess

class Box(object):
    ''' Base class representation for all machines '''
        
    def __init__(self):
        self.mach = "unknown"

    def images(self, filename):
        ''' Find an image stored in images/(mac/win/linux) or images directory'''
        directory = 'images' + SEPARATOR + self.mach + SEPARATOR
        if (os.path.isfile(PATH + directory + filename)):
            return PATH + directory + filename
        else:
            return PATH + 'images' + SEPARATOR + filename

class MacBox(Box):
    ''' A MacBox object will contain functions that are mac specific '''
    def __init__(self):
        super(MacBox, self).__init__()
        self.home = os.path.expanduser("~") + "/Applications/"
        self.mach = "mac"

    def nativediropen(self):
        '''nativediropen: will open the directory where the native application is installed
         this can be used in conjunction with the vision processing inside sikuli to verify 
         an application was installed
        '''
        subprocess.call(["open", self.home])

    def nativedirdeleteapps(self):
        ''' delete all the apps that are installed, this api needs to nativedirdelete(self, app) 
        nativedirdeleteapps will delete all the apps in the binary installed application '''
        subprocess.call(["rm", "-rf", self.home])

    def images(self, filename): 
        return super(MacBox, self).images(filename)

    def firefoxLocation(self):
        if(os.path.isdir('/Applications/Firefox.app/Contents/MacOS')):
            return '/Applications/Firefox.app/Contents/MacOS/firefox-bin'
        else:
            # XXX: Need to return proper error
            return 0

    def maximizeapp(self, app):
        ''' maximize the application that you pass in '''
        app.focus()
        print self.images("maximize_firefox.png")
        mTL = find(self.images("maximize_firefox.png"))
        dragDrop(mTL.getCenter().offset(50,0), Location(100,30))
        mLL = find(self.images("bottom_right.png"))
        reg = Screen(0).getBounds()
        dragDrop(mLL, Location(reg.width,reg.height))
    
class WinBox(Box):
    ''' A windows box will contain functions that are windows specific '''

    def __init__(self):
        super(WinBox, self).__init__()
        '''initializes the class '''
        self.home = os.getenv('APPDATA')
        self.mach = "windows"
  
    def images(self,filename):
        ''' images is custom for windows because their slashes are always the wrong way
            essence is to return all the images'''
        return super(WinBox, self).images(filename)
  
    def nativediropen(self):
        ''' Opening APPDATA in windows'''
        subprocess.call(["open", self.home])

    def nativedirdeleteapps(self):
        '''unimplemented in windows'''
        return 0
	
    def firefoxLocation(self):
        if(os.path.isdir('C:\\Program Files (x86)\\Mozilla Firefox\\')):
            return 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
        elif(os.path.isdir('C:\\Prgram Files\\Mozilla Firefox\\')):
            return 'C:\\Prgram Files\\Mozilla Firefox\\firefox.exe'
        else:
		    # XXX: Need to throw proper error
            return 0

    def maximizeapp(self, app):
        #XXX: Need to have better error handling depending on if app is already maximized or not
        maxButton = self.images("maximize_firefox_icon.png")
        click(maxButton)

class LinBox(Box):
    ''' linuxbox is currently untested, but will need to be filled in when appropriate '''
    def __init__(self):
        super(LinBox, self).__init__()
        self.home = os.path.expanduser("~") + "/Applications/"
        self.mach = "linux"

class System(object):
    '''  A call to the System class anywhere should return an object
       that is tailored to return operating system dependent data
    '''

    def __new__(cls):
        osname = str(MYOS).capitalize()
        klass = {
            'Linux': LinBox(),
            'Windows': WinBox(),
            'Mac': MacBox()
        }.get(osname, None)
        if not klass:
            raise Exception, 'Platform not supported'
        return klass
