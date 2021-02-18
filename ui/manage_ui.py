# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 08:49:34 2020

@author: 6065
"""

import os
import wx
import re
from pubsub import pub

class Manage(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent,style = wx.SIMPLE_BORDER)   # wx.SIMPLE_BORDER wx.RAISED_BORDER wx.SUNKEN_BORDER wx.NO_BORDER 
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        rm = ["All files (*.*)","Python files (*.py)","csv files (*.csv)","txt files (*.txt)"]        
        self.Manage_type = wx.ComboBox(self, 121,value="All files (*.*)",choices=rm,style=wx.CB_READONLY)       
        self.dir = wx.GenericDirCtrl(self, 122, os.path.dirname(os.path.abspath(__file__)), wx.DefaultPosition, (framew/5,frameh/2), wx.DIRCTRL_MULTIPLE, "All files (*.*)|*.*")      
        self.Manage_sizer = wx.BoxSizer(wx.VERTICAL)
        self.Manage_sizer.Add(self.dir, proportion=1, flag=wx.ALL, border=10)
        self.Manage_sizer.Add(self.Manage_type, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer( self.Manage_sizer )       
        self.Manage_type.Bind(wx.EVT_COMBOBOX, self.OnCombo)
        self.dir.Bind(wx.EVT_DIRCTRL_SELECTIONCHANGED, self.OnSelect)
        self.Layout()
        self.Hide()
        
    def OnCombo(self,event):
        Managefunc =  format(event.GetString())   
        Managefunc1 = Managefunc +'|'+ re.findall('\((.*?)\)',Managefunc)[0]
        self.Managefunc = Managefunc1
        self.curr_path = self.dir.GetPath()
        self.dir.SetFilter(self.Managefunc)
        self.dir.CollapseTree()
        self.dir.SetPath(self.curr_path)
    
    def OnSelect(self, event):
        self.curr_path = self.dir.GetPath()
        if self.curr_path:
            pub.sendMessage("path", path=self.curr_path)
        else: pass
        return self.curr_path