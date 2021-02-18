# -*- coding: utf-8 -*-
"""
Created on Wed May  8 22:57:15 2019

@author: ACER
"""
import glob
import inspect
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# from mpldatacursor import HighlightingDataCursor

path = 'C:/Users/6065/Desktop/830-00316-000_A_11819201103001_Station1_20201123100430.csv' 
data = pd.read_csv(path, engine='python')










    def update_path_via_pubsub(self, path):
        self.path = path     
    
    def Update_path(self, event):
        self.display_path = self.path


# 這裡不是字串的地方要先轉成字串
Class = data.loc[:,'class'].values
name = data.loc[:,'name'].values
channel = data.loc[:,'channel'].values
#NIRS_ictal_state = data.loc[:,'NIRS_ictal_state'].values
#sex = data.loc[:,'sex'].values

Mean = data.loc[:,'Mean'].values
Mean_s  = [str(i) for i in Mean]

peak = data.loc[:,'peak'].values
peak_s  = [str(i) for i in peak]

Var = data.loc[:,'Var'].values
Var_s = [str(i) for i in Var]

Skewtest = data.loc[:,'Skewtest'].values
Skewtest_s  = [str(i) for i in Skewtest]

Kurtosistest = data.loc[:,'Kurtosistest'].values
Kurtosistest_s  = [str(i) for i in Kurtosistest]

slope = data.loc[:,'slope'].values
slope_s  = [str(i) for i in slope]

activation = data.loc[:,'activation'].values
activation_s = [str(i) for i in activation]

age = data.loc[:,'age'].values
age_s = [str(i) for i in age]

#names = np.array(list("ABCDEFGHIJKLMNO"))

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

data['class']=data['class'].map({'HC':0,'CM':2,'MOH':2}).astype(int)

data['channel']=data['channel'].map({'ch1':0,'ch2':1,'ch3':2,'ch4':3}).astype(int)
#data['channel']=data['channel'].map({'ch12':0,'ch34':2}).astype(int)

##data['NIRS_ictal_state'] =data['NIRS_ictal_state'].map({'HC or interictal':0,'Ictal_scan during any head pain':2}).astype(int)
#data['sex']=data['sex'].map({'F':0,'M':2}).astype(int)


x = Mean                        # 選擇x軸要放的 feature
y = peak                        # 選擇y軸要放的 feature
c = data.loc[:,'class'].values    # 選擇要標記成不同顏色的項目 (數值表示)
#c = data.loc[:,'channel'].values      # 選擇要標記成不同顏色的項目 (數值表示)


#c = np.random.randint(0,1255,size=33)
#s = np.linspace(100,100,33)

norm = plt.Normalize(1,4)  # 亮度調整到 1~4
cmap = plt.cm.RdYlGn

x_name = retrieve_name(x)
y_name = retrieve_name(y)
fig,ax = plt.subplots()
plt.xlabel(x_name)
plt.ylabel(y_name)
sc = plt.scatter(x,y,c=c, s=100, cmap=cmap, norm=norm)  #做散佈圖

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",  
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))


   # plt.fill_between(Time_Host,data_yaxis,data_yaxis1, where= run_times==j,facecolor='beige')

# xy：被註釋的座標點，二維元組形如(x,y)
# xytext：註釋文字的座標點，也是二維元組，預設與xy相同
# xycoords：被註釋點的座標系屬性，允許輸入的值如下 'figure points', 'figure pixels'...
# textcoords ：註釋文字的座標系屬性，預設與xycoords屬性值相同，也可設為不同的值。除了允許輸入xycoords的屬性值，還允許輸入以下兩種
#              'offset points'	相對於被註釋點xy的偏移量（單位是點）
#              'offset pixels'	相對於被註釋點xy的偏移量（單位是畫素）
# arrowprops：箭頭的樣式，dict（字典）型資料，如果該屬性非空，則會在註釋文字和被註釋點之間畫一個箭頭。如果不設定'arrowstyle' 關鍵字，則允許包含以下關鍵字：
#             width	箭頭的寬度（單位是點）
#             headwidth	箭頭頭部的寬度（點）
#             headlength	箭頭頭部的長度（點）
#             shrink	箭頭兩端收縮的百分比（佔總長）

# 如果設定了‘arrowstyle’關鍵字，以上關鍵字就不能使用。允許的值有：
#     '-'	None
#     '->'	head_length=0.4,head_width=0.2
#     '-['	widthB=1.0,lengthB=0.2,angleB=None ...


annot.set_visible(False)

def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}, {},{}".format( 
                            " ".join([channel[n] for n in ind["ind"]]),
                            " ".join([age_s[n] for n in ind["ind"]]),
                            " ".join([name[n] for n in ind["ind"]]),
                            " ".join([Class[n] for n in ind["ind"]]))  
    '''     可在這裡加上多項要標註的內容，方法按上面操作即可    '''
    #" ,".join(list(map(str,ind["ind"]))),  # 加上 index                          
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()
                

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()




#%%
# 另一種畫法

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





