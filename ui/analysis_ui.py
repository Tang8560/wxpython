# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 08:51:28 2020

@author: 6065
"""

import os
import wx
from pubsub import pub


## 嵌入圖片到wxpython ##
from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

class ControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.control_sizer = wx.BoxSizer(wx.VERTICAL)
        self.control_sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.control_sizer)
        self.Fit()
        
class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.draw()
        self.canvas_sizer = wx.BoxSizer(wx.VERTICAL)
        self.canvas_sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.canvas_sizer)
        self.Fit()

    def draw(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)


class Analysis_mode(wx.Panel):
    def __init__(self, parent):       
        super().__init__(parent)   
        pub.subscribe(self.update_path_via_pubsub, "path")

        self.SetBackgroundColour("green")
        self.display_path = os.path.abspath(__file__)
        
        self.analysismode_sizer = wx.BoxSizer( wx.HORIZONTAL )
        
        # TASK PANEL
        self.analysis_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.panle_sizer = wx.BoxSizer( wx.VERTICAL )    
        self.analysis_text = wx.TextCtrl( self.analysis_panel, wx.ID_ANY, self.display_path, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.panle_sizer.Add( self.analysis_text, 0, wx.EXPAND | wx.ALL, 5 ) 
        self.panle_sizer.Add( CanvasPanel(self), 0, wx.EXPAND | wx.ALL, 5 ) 
        self.analysis_panel.SetSizer(self.panle_sizer) 
        self.analysis_panel.Layout()
        self.panle_sizer.Fit( self.analysis_panel )
        self.analysismode_sizer.Add( self.analysis_panel, 2, wx.EXPAND |wx.ALL, 5 )
        
        
        # LAYOUT
        self.SetSizer( self.analysismode_sizer )
        self.Layout()
        
    def update_path_via_pubsub(self, path):
        self.path = path     
    

        
        
        
        
        
        
        
        
        

'''
import matplotlib.pyplot as plt
import numpy as np
import mplcursors

path = 'C:/Users/ACER/Desktop/fNIRS/SVM3.csv'  
data = pd.read_csv(path, engine='python')
data['class']=data['class'].map({'HC':0,'CM':1,'MOH':2}).astype(int)
x = data.loc[:,'Mean'].values
y = data.loc[:,'Peak'].values
c = data.loc[:,'class'].values


fig, ax = plt.subplots()
lines = ax.scatter(x,y)
ax.set_title("Click somewhere on a line.\nRight-click to deselect.\n"
             "Annotations can be dragged.")

mplcursors.cursor(lines) # or just mplcursors.cursor()

plt.show()
'''        
        
        
        
        
        
        
        