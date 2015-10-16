#!/usr/bin/env python
import wx
import urllib2
import sys

# if you want debug application
IS_DEBUG = False
# default id to control timer (loop)
ID_ICON_TIMER = wx.NewId()

# Default text to show on mouseover icon
TRAY_TOOLTIP    = 'Check Internet Connection - '
# icon to show on internet connected
TRAY_ICON_ON    = 'internet_on.png'
# icon to show on internet NOT connected
TRAY_ICON_OFF   = 'internet_off.png'

class TaskBarFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, style=wx.FRAME_NO_TASKBAR | wx.NO_FULL_REPAINT_ON_RESIZE)
        
        # create icon
        self.tbicon = wx.TaskBarIcon()
        icon = wx.Icon(TRAY_ICON_OFF, wx.BITMAP_TYPE_PNG)
        self.tbicon.SetIcon(icon, TRAY_TOOLTIP + 'Starting...')

        # events click on icon in taskbar
        wx.EVT_TASKBAR_LEFT_DCLICK(self.tbicon, self.OnTaskBarLeftDClick)
        wx.EVT_TASKBAR_RIGHT_UP(self.tbicon, self.OnTaskBarRightClick)

        self.auto_update()
        self.Show(True)

    def auto_update(self):
        self.SetIconTimer()

    def OnTaskBarLeftDClick(self, evt):
        if IS_DEBUG:
            print 'Double click left'

        try:
            self.icontimer.Stop()
        except:
            pass

        icon = wx.Icon(TRAY_ICON_OFF, wx.BITMAP_TYPE_PNG)
        self.tbicon.SetIcon(icon, TRAY_TOOLTIP + 'Checking...')

        self.SetIconTimer()

    def OnTaskBarRightClick(self, evt):
        if IS_DEBUG:
            print 'You click with right click'
        self.Close(True)
        sys.exit()

    def SetIconTimer(self):
        self.icontimer = wx.Timer(self, ID_ICON_TIMER)
        wx.EVT_TIMER(self, ID_ICON_TIMER, self.on_verify_connection)
        self.icontimer.Start(30000)

    # to understand method used by Windows see:
    # https://technet.microsoft.com/en-us/library/cc766017%28WS.10%29.aspx?f=255&MSPPError=-2147217396
    # dns to: 131.107.255.255(dns.msftncsi.com)
    def check_connection(self):
        try:
            response=urllib2.urlopen('http://www.msftncsi.com/ncsi.txt', timeout=1)
            return True
        except urllib2.URLError as err: pass
        return False

    def on_verify_connection(self, evt):
        self.verify_connection()

    def verify_connection(self):
        
        if self.check_connection():
            icon = wx.Icon(TRAY_ICON_ON, wx.BITMAP_TYPE_PNG)
            self.tbicon.SetIcon(icon, TRAY_TOOLTIP + 'ON')

            if IS_DEBUG:
                print 'Connected'
        else:
            icon = wx.Icon(TRAY_ICON_OFF, wx.BITMAP_TYPE_PNG)
            self.tbicon.SetIcon(icon, TRAY_TOOLTIP + 'OFF')
            
            if IS_DEBUG:
                print 'Not Connected'

# load and start application frame
app = wx.App(False)
frame = TaskBarFrame(None)
frame.Show(False)
app.MainLoop()