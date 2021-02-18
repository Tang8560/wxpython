# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 08:50:48 2020

@author: 6065
"""

import os
import wx
from pubsub import pub

class Display_mode(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        pub.subscribe(self.update_path_via_pubsub, "path")

        self.SetBackgroundColour("red")
        self.display_path = os.path.abspath(__file__)
       
    def update_path_via_pubsub(self, path):
        self.path = path     
    

        
        
# class Open(wx.Panel):
#     from win32com.client import DispatchEx
#     filename, file_extension = os.path.splitext(self.path)
    
#     if file_extension == '.csv': 
#         excel = DispatchEx("Excel.Application")
#         excel.Visible = 1
#         excel.Workbooks.Open("somefile.csv")
#         excel.Save("somefile.csv")
        
#     elif file_extension == '.ppt': 
#         ppt = Dispatch("PowerPoint.Application")
#         ppt.Visible = 1
#         ppt.Workbooks.Open("somefile.ppt")
#         ppt.Save("somefile.ppt")

#     elif file_extension == '.docx': 
#         ppt = Dispatch("Word.Application")
#         ppt.Visible = 1
#         ppt.Workbooks.Open("somefile.docx")
#         ppt.Save("somefile.ppt")

#     else: 
#         osCommandString = "notepad.exe file.txt"
#         os.system(osCommandString)

        
        
# class Notebook(wx.Notebook):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.task_panel = Task_mode(self)
#         self.display_panel = Display_mode(self)
#         self.analysis_panel = Analysis_mode(self)
#         self.AddPage( self.task_panel,"", True )
#         self.AddPage( self.display_panel,"", True )
#         self.AddPage( self.analysis_panel,"", True )