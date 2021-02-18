# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 16:31:29 2020

@author: 6065
"""
import os
import re
import wx
import wx.grid
import pandas as pd


def Data():
    new_data = list(filter(None, [re.split('\t', i.strip('\n')) for i in open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ '\\config\\'+'Test Spec.ini', newline = '')]))
    result = pd.DataFrame(new_data)
    
    header = result.transpose()[0][1:10]
    body = result[1:-1].transpose().values.tolist()
    
    data_embedded = dict(zip(header, body))
    data = {"Task flow":[data_embedded]}
    
    return data

data = Data()


## 匯入資料的形式 ##
## 可以利用名稱選擇匯入不同的資料 ##
# data = {"Task flow": [
#         {   "titles": ["example123456789", "exampletitle2"],
#             "author": ["author123456", "author2"],
#             "urls"  : ["123/", "1"],
#             "urls1" : ["123/", "1"],
#             "urls2" : ["123/", "1"],
#             "urls3" : ["123/", "1"],       }     ],
#    "XXX" : [{ }]
# }

EVEN_ROW_COLOUR = '#CCE6FF'
GRID_LINE_COLOUR = '#ccc'

# Declare DataTable to hold the wx.grid data to be displayed
class DataTable(wx.grid.GridTableBase):
    def __init__(self, data=None):
        wx.grid.GridTableBase.__init__(self)
        self.headerRows = 1
        if data is None:
            data = pd.DataFrame()
        self.data = data

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data.columns) + 1

    def GetValue(self, row, col):
        if col == 0:
            return self.data.index[row]
        return self.data.iloc[row, col - 1]

    def SetValue(self, row, col, value):
        self.data.iloc[row, col - 1] = value

    def GetColLabelValue(self, col):
        if col == 0:
            if self.data.index.name is None:
                return 'Index'
            else:
                return self.data.index.name
        return str(self.data.columns[col - 1])

    def GetTypeName(self, row, col):
        return wx.grid.GRID_VALUE_STRING

    def GetAttr(self, row, col, prop):
        attr = wx.grid.GridCellAttr()
        if row % 2 == 1:
            attr.SetBackgroundColour(EVEN_ROW_COLOUR)
        return attr


class Task_Grid(wx.Panel):
    """
    Frame that holds all other widgets
    """

    def __init__(self, parent):
        """Constructor"""
        
        super().__init__(parent) 
        self._init_gui()

    def _init_gui(self):
        # assign the DataFrame to df
        df = pd.DataFrame(data["Task flow"][0])
        table = DataTable(df)
        print(table)

        #declare the grid and assign data
        self.grid = wx.grid.Grid(self, -1, style = wx.VSCROLL )
        self.grid.HideRowLabels()             # grid.SetRowLabelSize( 0 )
        self.grid.SetTable(table, takeOwnership=True)
        # grid.AutoSizeColumns()
                
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)        
        self.mainSizer.Add(self.grid, 0, wx.EXPAND) 
        self.SetSizer(self.mainSizer)
        self.Layout()
        self.mainSizer.Fit(self)

        self.Bind(wx.EVT_CLOSE, self.exit)
            
        ## 因為外層的frame會做最大化，而這裡的Sizer是在最大化前抓的，所以值會不同，需綁定視窗變化事件 ##
        # ss = self.GetSize()
        self.Bind(wx.EVT_SIZE, self.OnResize)    

    def exit(self, event):
        self.Destroy()
     
    ## 在task_ui中也需要引入OnResize的功能 ##
    def OnResize(self, event):
        ss = self.GetSize()


        for i in range(self.grid.GetNumberCols()):
            self.grid.SetColSize(i,ss[0]/(self.grid.GetNumberCols()))
        
        ## 在Sizer因為有物件移除而產生變動時不需要去Fit或SetSizer，才不會造成滾動條的消失 ##
        ## Fit的目的是是告訴Sizer去重設視窗的大小以使當前區域符合最小大小 ##
        ## SetSizer 面板以此決定順序加入頂層 ##
        ## 記得要先Layout，格式才不會跑掉 ##    
        
        # self.mainSizer.Fit(self)
        # self.SetSizer(self.mainSizer)
        self.Layout()
    