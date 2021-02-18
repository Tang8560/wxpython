# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 15:46:26 2021

@author: 6065
"""
import wx
import sys

class RedirectText(object):
    """Redirect command prompt to the ATS GUI"""
    def __init__(self,aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)
        
class AuiFrame(wx.Panel):
    
    def __init__(self, parent):
        super().__init__(parent)
        ## 可停靠視窗 ##
        self.mgr = wx.lib.agw.aui.AuiManager()
        self.mgr.SetManagedWindow(self)        

        ## TASK RIGHT PANEL ##
        self.aui_panel1 = wx.Panel( self )
        self.aui_panel1.Hide()
        auiinfo1 = wx.lib.agw.aui.AuiPaneInfo().Caption('Python Shell').BestSize((300, 300))\
                    .CloseButton(True).MaximizeButton(True).MinimizeButton(True).Show().Floatable(False)\
                    .Dockable(True).Center().GripperTop(True).Movable(True)   # .DestroyOnClose(False)

        self.aui_panel2 = wx.Panel( self )     
        self.aui_panel2.SetBackgroundColour('red')          
        self.console_text = wx.TextCtrl( self.aui_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.VSCROLL|wx.TE_MULTILINE ) 
        self.aui_panel2.Hide() 
        auiinfo2 = wx.lib.agw.aui.AuiPaneInfo().Caption('Python Console').BestSize((300, 300))\
                    .CloseButton(True).MaximizeButton(True).MinimizeButton(True).Show().Floatable(False)\
                    .Dockable(True).Center().GripperTop(True).Movable(True)   # .DestroyOnClose(False)
        
        ns = {}
        ns['wx'] = wx
        ns['app'] = wx.GetApp()
        ns['frame'] = self.aui_panel1
        self.shell = wx.py.shell.Shell(self.aui_panel1, -1, locals=ns)

        self.mgr.AddPane(self.shell, auiinfo1)
        self.mgr.AddPane(self.console_text, auiinfo2, target=auiinfo1)  
        self.mgr.Update()
        # self.mgr.Bind(wx.lib.agw.aui.EVT_AUI_PANE_CLOSE, self.aui_close)       
        
        redir = RedirectText(self.console_text)
        sys.stdout = redir

           
    def __OnQuit(self, event):
        self.mgr.UnInit()
        del self.mgr
        self.Destroy()

        
    def OnRemove(self, sizer, *args):
        """arg: the order on the sizer (int)"""
        for arg in args:
            sizer.Hide(arg)
            sizer.Remove(arg)
            sizer.Layout()