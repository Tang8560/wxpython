# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 12:56:44 2020

@author: 6065
"""


import os
import wx
import wx.py
from wx.adv import SplashScreen
from pubsub import pub
from ui.tool_ui import Tool
from ui.manage_ui import Manage
from ui.aui_ui import AuiFrame
from ui.task_ui import Task_mode
from ui.display_ui import Display_mode
from ui.analysis_ui import Analysis_mode    
       
class Main(wx.Frame):
    def __init__(self):
        self.path = ""
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        wx.Frame.__init__(self, None, title=u"ATS Manager" ,size=(framew, frameh)) 
        self.SetMinSize((framew/2, frameh/1.5))
        pub.subscribe(self.update_path_via_pubsub, "path")
        
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        
        self.tool =Tool(self)
        self.manage = Manage(self)
        self.auiframe = AuiFrame(self)
        self.taskmode = Task_mode(self)
        self.displaymode = Display_mode(self)
        self.analysismode = Analysis_mode(self)
        
        self.Menu()
        self.Status()
        self.InitUI()
        
    def Menu(self): 
        self.menubar = wx.MenuBar()
        self.File = wx.Menu()
        self.Open = wx.MenuItem( self.File, 101, "&Open\tCtrl+O", "Open file", wx.ITEM_NORMAL )
        self.Save = wx.MenuItem( self.File, 102, "&Save\tCtrl+S", "Save file", wx.ITEM_NORMAL )
        self.Quit = wx.MenuItem( self.File, 103, "&Quit\tCtrl+Q", wx.EmptyString, wx.ITEM_NORMAL ) 
        # self.Open.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_MENU,(16,16)))
        open_image = wx.Image('src/open.png').Rescale(16, 15)
        save_image = wx.Image('src/save.png').Rescale(16, 16)
        quit_image = wx.Image('src/quit.png').Rescale(16, 16)
        self.Open.SetBitmap(wx.Bitmap(open_image)) 
        self.Save.SetBitmap(wx.Bitmap(save_image)) 
        self.Quit.SetBitmap(wx.Bitmap(quit_image))             
        self.File.Append( self.Open )         
        self.File.Append( self.Save )
        self.File.AppendSeparator()
        self.File.Append( self.Quit )        
        self.menubar.Append( self.File, u" File " )
        
        self.Mode  = wx.Menu()
        self.Task = wx.MenuItem( self.Mode, 104, u"Task", wx.EmptyString, wx.ITEM_NORMAL ) 
        self.Display  = wx.MenuItem( self.Mode, 105, u"Display", wx.EmptyString, wx.ITEM_NORMAL )        
        self.Analysis = wx.MenuItem( self.Mode, 106, u"Analysis", wx.EmptyString, wx.ITEM_NORMAL ) 
        self.Settings = wx.MenuItem( self.Mode, 107, u"Settings", wx.EmptyString, wx.ITEM_NORMAL ) # wx.ITEM_RADIO
        task_image = wx.Image('src/task.png').Rescale(16, 16)
        display_image = wx.Image('src/display.png').Rescale(16, 16)
        analysis_image = wx.Image('src/analysis.png').Rescale(16, 16)
        self.Task.SetBitmap(wx.Bitmap(task_image)) 
        self.Display.SetBitmap(wx.Bitmap(display_image)) 
        self.Analysis.SetBitmap(wx.Bitmap(analysis_image))     
        self.Mode.Append( self.Task )
        self.Mode.Append( self.Display )
        self.Mode.Append( self.Analysis )
        self.Mode.AppendSeparator()
        self.Mode.Append( self.Settings )
        self.menubar.Append( self.Mode, u" Mode " ) 
        
        self.Help = wx.Menu()
        self.About = wx.MenuItem( self.Help, 108, u"About"+ u"\t" + u"F1", wx.EmptyString, wx.ITEM_NORMAL )       
        self.About.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_MENU,(16,16))) 
        self.Help.Append( self.About )
        self.menubar.Append( self.Help, u" Help " )         
        self.SetMenuBar( self.menubar )
        
        self.Bind(wx.EVT_MENU, self.tool.OnOpen,     id = 101) 
        self.Bind(wx.EVT_MENU, self.tool.OnSave,     id = 102) 
        self.Bind(wx.EVT_MENU, self.OnQuit,     id = 103)
        self.Bind(wx.EVT_MENU, self.OnTask,     id = 104) 
        self.Bind(wx.EVT_MENU, self.OnDisplay,  id = 105) 
        self.Bind(wx.EVT_MENU, self.OnAnalysis, id = 106) 
        self.Bind(wx.EVT_MENU, self.OnSettings, id = 107)
        self.Bind(wx.EVT_MENU, self.OnAbout,    id = 108)
    
    def Status(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-8,-1,-1])
        self.statusbar.SetStatusText("UTF-8",1)

        ## 計時工具 ##     
        self.timer = wx.Timer(self)  
        self.total_seconds = 0
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
    
    ## 計時工具 status 3 ##     
    def update(self, event):      
        self.total_seconds += 1
        second = self.total_seconds % 60
        minute = int((self.total_seconds / 60) % 60)
        hour = int((self.total_seconds / 3600) % 24)
        time = str(hour).zfill(2)+":"+str(minute).zfill(2)+":"+str(second).zfill(2)
        self.statusbar.SetStatusText("Run Time:     "+ time, 2 ) 
        
    def update_path_via_pubsub(self, path):
        self.path = path           
    
    def Update_path(self, event):
        self.path_txt.SetValue(self.path)
                 
    def InitUI(self): 
        self.SetBackgroundColour("white")       
        self.path_txt = wx.TextCtrl( self, 113, " " ,style = wx.TE_LEFT)        
        self.manage.Show()
        self.manageon_btn = wx.ToggleButton( self, -1, u'\u25c4', wx.DefaultPosition, (12,-1), wx.BORDER_NONE) # 25ba
        self.manageon_btn.SetFont( wx.Font( 10 , wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI Semibold" ) )      
        self.tool_sizer = wx.BoxSizer( wx.VERTICAL )     
        self.tool_sizer.Add(self.tool, 0, wx.EXPAND )
        self.tool_sizer.Add(self.path_txt, 0, wx.EXPAND )  
        self.framework_sizer = wx.BoxSizer( wx.HORIZONTAL )  
        self.framework_sizer.Add(self.manageon_btn, 0, wx.EXPAND |wx.RIGHT, 5 ) 
        self.framework_sizer.Add(self.manage, 0, wx.EXPAND)
        self.framework_sizer.Add(self.taskmode, 1, wx.EXPAND)
        self.framework_sizer.Add(self.auiframe, 1, wx.EXPAND)
        self.displaymode.Hide() 
        self.analysismode.Hide()
        
        self.manageon_btn.Bind(wx.EVT_TOGGLEBUTTON, self.OnClose) 
        self.tool.Bind(wx.EVT_TOOL, self.OnTask, id = 111)
        self.tool.Bind(wx.EVT_TOOL, self.OnDisplay, id = 112)
        self.tool.Bind(wx.EVT_TOOL, self.OnAnalysis, id = 113)
        
        
        # Use for pubsub --> get manage.dir path to pass path_txt
        self.manage.dir.Bind(wx.EVT_DIRCTRL_FILEACTIVATED, self.Update_path) 
        self.tool_sizer.Add(self.framework_sizer,1, wx.EXPAND | wx.ALL, 5 )  
        self.Centre( wx.BOTH ) 
        self.SetSizer(self.tool_sizer)   # self.Fit()   # self.FitInside()
        self.SetAutoLayout(True)
        self.Fit()
        self.Maximize(True)
        self.Show(True)
        self.path_txt.SetValue(os.path.abspath(__file__))
                
        
    def OnTask(self, event):
        if self.manageon_btn.GetLabel() == u"\u25ba":
            self.OnRemove(self.framework_sizer,1)
            
        else:    
            self.OnRemove(self.framework_sizer,2)
        self.taskmode.Hide()
        self.displaymode.Hide() 
        self.analysismode.Hide()         
        self.framework_sizer.Add(self.taskmode, 1, wx.EXPAND )
        self.taskmode.Show()
        self.framework_sizer.Layout() 
        
    def OnDisplay(self, event):
        if self.manageon_btn.GetLabel() == u"\u25ba":
            self.OnRemove(self.framework_sizer,1)
        else:    
            self.OnRemove(self.framework_sizer,2)
        self.taskmode.Hide()
        self.displaymode.Hide() 
        self.analysismode.Hide()            
        self.framework_sizer.Add(self.displaymode, 1, wx.EXPAND)
        self.displaymode.Show()
        self.framework_sizer.Layout() 
        
    def OnAnalysis(self, event):
        if self.manageon_btn.GetLabel() == u"\u25ba":
            self.OnRemove(self.framework_sizer,1)
        else:    
            self.OnRemove(self.framework_sizer,2)
        self.taskmode.Hide()
        self.displaymode.Hide() 
        self.analysismode.Hide()    
        self.framework_sizer.Add(self.analysismode, 1, wx.EXPAND )
        self.analysismode.Show()
        self.framework_sizer.Layout() 
    
    def OnSettings(self, event):
        pass
    
    def OnQuit(self, event):
        dlg=wx.MessageDialog(None,u"Are you sure you want to close the window?",u"Confirm close",wx.YES_NO)         
 
        if dlg.ShowModal()==wx.ID_YES:
                       
            ## RuntimeError: wrapped C/C++ object of type TextCtrl has been deleted
            ## 主線程關閉了但其他線程還在訪問 --> 取消pubsub的訂閱 --> pub.unsubscribe
            ## C++ assertion "GetEventHandler() == this" failed at ..\..\src\common\wincmn.cpp(475) in wxWindowBase::~wxWindowBase(): 
            ## any pushed event handlers must have been removed
            ## 所有推播程序都要關閉 --> pub.unsubAll
            ## https://pypubsub.readthedocs.io/en/v4.0.3/usage/module_pub.html
            ## 取消所有pubsub的訂閱 ##  (切記要是所有)
            try:
                self.taskmode.mgr.UnInit()
                pub.unsubAll("path")             
            except: pass
            print("Exit the program : [True] ")
            wx.CallAfter(self.Destroy)
            
            ## Veto（）用於防止事件的處理，而Skip（）允許事件的傳播和“更多”事件的處理
            event.Veto()

        else:
            print("Exit the program : [False] ")
            return 
    
    def OnAbout(self, event):
        pass
        
    def OnClose(self, event):
        button = event.GetEventObject()
        if button.GetValue() == True:    
            self.OnRemove(self.framework_sizer,1)
            # 因為sizer.Remove只會將物件從Sizer中移除，物件仍會出現在panel上造成物件重疊的畫面
            # 因此remove要再將物件做隱藏的動作
            self.manage.Hide()
            self.SetSizer(self.tool_sizer)
            button.SetLabel(u"\u25ba")     
        else:
            self.manage.Show()
            self.framework_sizer.Insert(1, self.manage,  0, wx.EXPAND)
            self.manage.dir.Bind(wx.EVT_DIRCTRL_FILEACTIVATED, self.Update_path)
            self.framework_sizer.Layout()
            button.SetLabel(u"\u25c4") 

    def OnRemove(self, sizer, *args):
        """arg: the order on the sizer (int)"""
        for arg in args:
            sizer.Hide(arg)
            sizer.Remove(arg)
            sizer.Layout()


class Splash(SplashScreen):
    __doc__ = SplashScreen.__doc__
    
    def __init__(self):  
        try:
            img = wx.Image('src/splash.jpg',wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            img = wx.Bitmap(img)
            SplashScreen.__init__(self, img, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT, 2000, None, -1)
            self.Bind(wx.EVT_CLOSE, self.OnClose)
            self.fc = wx.CallLater(1000, self.ShowMain)
        except Exception as e:
            print(e)


    def OnClose(self, evt):
        # Make sure the default handler runs too so this window gets destroyed
        evt.Skip()
        self.Hide()

        # if the timer is still running then go ahead and show the main frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()

    def ShowMain(self):
        frame = Main()
        frame.Show()
        if self.fc.IsRunning():
            self.Raise()
        wx.CallAfter(frame.Show)
        
        
if __name__ == '__main__':  
    app = wx.App()
    win = Splash()
    app.MainLoop()


