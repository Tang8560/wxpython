# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 08:50:02 2020

@author: 6065
"""

import os
import sys
import wx
import wx.lib.agw.aui
from pubsub import pub
from ui.task_grid import Task_Grid
# from ui.manage_ui import Manage

class Task_mode(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)   
        pub.subscribe(self.update_path_via_pubsub, "path")

        self.display_path = os.path.abspath(__file__)
        self.taskmode_sizer = wx.BoxSizer( wx.VERTICAL)
        
        ## TASK PANEL ##
        self.SetBackgroundColour("#FFFAF0")
        self.subsizer = wx.BoxSizer( wx.VERTICAL )
        self.subsizer1 = wx.BoxSizer( wx.HORIZONTAL )
        self.subsizer2 = wx.BoxSizer( wx.VERTICAL )
        self.subsizer3 = wx.BoxSizer( wx.VERTICAL )
        self.subgsizer1 = wx.GridSizer( 0, 2, 1, 1 )

        self.serialnum = wx.StaticText( self, -1, "Serial Number" )
        self.serial_txt = wx.TextCtrl( self, -1 ,style = wx.TE_CENTRE)
        
        self.start_btn = wx.Button( self, -1, "Start")
        self.stop_btn = wx.Button( self, -1, u"Stop")
        self.change_btn = wx.Button( self, -1, u"ChangeUser")
        self.manual_btn = wx.Button( self, -1, u"Manual Panel" )
        
        self.subgsizer1.Add( self.start_btn, 0, wx.ALL|wx.EXPAND, 5 )
        self.subgsizer1.Add( self.stop_btn,  0, wx.ALL|wx.EXPAND, 5 )
        self.subgsizer1.Add( self.change_btn, 0, wx.ALL|wx.EXPAND, 5 )
        self.subgsizer1.Add( self.manual_btn, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        self.subsizer3.Add( self.serial_txt, 0, wx.ALL|wx.EXPAND, 5 )       		
        self.subsizer2.Add( self.serialnum, 1, wx.ALL, 5 )
        
        
        self.subsizer1.Add( self.subsizer2, 0, wx.EXPAND )
        self.subsizer3.Add( self.subgsizer1, 0, wx.EXPAND )
        self.subsizer1.Add( self.subsizer3, 0, wx.EXPAND )
        self.subsizer.Add( self.subsizer1, 0, wx.EXPAND )
        
        # 檢查 Task_ui 傳入的地址是否正確
        # self.task_text = wx.TextCtrl( self.task_panel, wx.ID_ANY, self.display_path, wx.DefaultPosition, wx.DefaultSize, 0 )
        # self.panel_sizer.Add( self.task_text, 1, wx.EXPAND | wx.ALL, 5 )   
        
        self.taskmode_sizer.Add( self.subsizer, 0, wx.ALL, 5 )
        self.staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        self.taskmode_sizer.Add( self.staticline1, 0, wx.EXPAND |wx.ALL, 5 )    
        self.taskmode_sizer.Add( Task_Grid(self), 1, wx.EXPAND | wx.ALL, 5 ) 
           

        self.taskmode_sizer.Fit(self)       
        self.SetSizer(self.taskmode_sizer)
        self.Layout() 
        
    def update_path_via_pubsub(self, path):    
        self.path = path
        print('******************************')
        print(self.path)
        ## 更新Task mode的路徑 ##
        # self.task_text.SetValue(self.path)
