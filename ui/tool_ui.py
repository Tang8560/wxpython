# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 08:48:51 2020

@author: 6065
"""

import wx

class Tool(wx.ToolBar):
    def __init__(self, parent):
        super().__init__(parent, style = wx.TB_FLAT)
        self.toolbar_ret = 'Task_mode'
        # self.SetBackgroundColour("white")
        self.SetTransparent(100)
        open_image = wx.Image('src/open.png').Rescale(32, 30)
        save_image = wx.Image('src/save.png').Rescale(32, 32)
        task_image = wx.Image('src/task.png').Rescale(32, 32)
        display_image = wx.Image('src/display.png').Rescale(32, 32)
        analysis_image = wx.Image('src/analysis.png').Rescale(32, 32)
        self.AddTool( 109, 'open', wx.Bitmap(open_image))  
        self.AddTool( 110, 'save', wx.Bitmap(save_image))
        self.AddSeparator() 
        self.AddTool( 111, 'task', wx.Bitmap(task_image))  
        self.AddTool( 112, 'display', wx.Bitmap(display_image)) 
        self.AddTool( 113, 'analysis', wx.Bitmap(analysis_image))  
        self.Realize() 
        self.Bind(wx.EVT_TOOL, self.OnOpen, id = 109)
        self.Bind(wx.EVT_TOOL, self.OnSave, id = 110)
        
    def OnOpen(self, event):
        filepath = wx.FileDialog(self,u"Open file","","","",wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if filepath.ShowModal() == wx.ID_OK:
            self.taskpath = filepath.GetPath()
        else: return
    def OnSave(self, event):
        pass