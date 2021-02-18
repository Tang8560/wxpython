# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:38:48 2021

@author: 6065
"""

import wx

class Task_Control(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent) 
        self.ts_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.panel_sizer = wx.BoxSizer( wx.VERTICAL )
        self.task_text = wx.TextCtrl( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.panel_sizer.Add( self.task_text, 1, wx.EXPAND | wx.ALL, 5 )
        self.SetSizer( self.panel_sizer )
        self.Layout()
        self.Fit()