import pandas as pd
import os
import numpy as np
import re
import plotly.graph_objects as go
import pylab as p


def to_int(str):
    if str == 'Fail':
        return -1
    elif str == 'Pass':
        return 1
    else:
        return 0


class SHMViewer():

    def __init__(self, txt):
        self.content = txt
        self.pattern = ''
        self.head = ''
        # match pattern for all shmoo data
        self.shm_pattern = r'Time Stamp'
        # match pattern for head file of each shmoo
        self.head_pattern = r'Program Info.*Context'
        # match pattern content of each shmoo
        self.pattern_format = r'Site.*'

    def match_pattern(self):
        shmoos = re.split(self.shm_pattern,self.content)
        if shmoos:
            print("匹配成功！")
        else:
            print("匹配失败！")
        #print(shmoos[0])
        return shmoos[1:]

    def show_headfile(self,txt):
        self.head = re.findall(self.head_pattern,txt,re.DOTALL)[0]
        return self.head

    def plot_shm(self,txt):
        title = self.get_tname()
        print(title)

        self.pattern = re.findall(self.pattern_format, txt,re.DOTALL)[0]

        xdata,ydata,zdata,textdata,xaxis,yaxis = self.get_shm()

        layout = go.Layout(
            plot_bgcolor='#F7F7F7',  # 图的背景颜色 #F8F8FF
            paper_bgcolor='#F0F8FF',  # 图像的背景颜色
            title=title,  # Title
            titlefont=dict(color='rgb(148, 103, 189)', size=16),
            # 设置x轴的刻度和标签
            xaxis=dict(title=xaxis,  # 设置坐标轴的标签
                       titlefont=dict(color='rgb(148, 103, 189)', size=12),
                       tickfont=dict(color='rgb(148, 103, 189)', size=12),
                       #tickmode='linear',
                       showgrid=False,
                       showline=False,
                       gridcolor='black',
                       gridwidth=2,
                       linecolor='#636363',
                       linewidth=2),

            yaxis=dict(title=yaxis,  # 设置坐标轴的标签
                       #position=dict(l=40, r=30, t=10, b=20),
                       titlefont=dict(color='rgb(148, 103, 189)', size=12),  # 设置坐标轴标签的字体及颜色
                       tickfont=dict(color='rgb(148, 103, 189)', size=12),  # 设置刻度的字体大小及颜色
                       #tickmode='linear',
                       showgrid=False,
                       showline=False,
                       gridcolor='black',
                       gridwidth=2,
                       linecolor='#636363',
                       linewidth=2),
            # 设置图例
            legend=dict(x=0.2, y=1.3,  # 设置图例的位置，[0,1]之间
                        font=dict(family='sans-serif', size=13, color='black'),  # 设置图例的字体及颜色
                        bgcolor='#F8F8FF', bordercolor='#FFFFFF'),  # 设置图例的背景及边框的颜色
            showlegend=True)  # 设置不显示图例
        fig = go.Figure(layout=layout)

        fig.add_trace(go.Heatmap(z=zdata,
                                   x=xdata,
                                   y=ydata,
                                   colorscale=['#ff3030', '#3D9970','#afeeee'] ,
                                   text=textdata,
                                   xgap=1,
                                   ygap=1,
                                   showscale=False,
                                   showlegend=False,
                                   #connectgaps=False
                                   ))
        fig.update_xaxes(type='category')  # 将x轴设置为类别类型
        fig.update_yaxes(type='category')  # 将y轴设置为类别类型
        fig.update_layout(
            margin=dict(l=120, r=50, t=80, b=100)
        )

        return fig

    def show_tail(self,txt):
        tail = re.findall(r'SITE\s+\d+.*SHMOO over!', txt,re.DOTALL)[0]
        return tail

    def get_shm(self):
        x_index=[]
        y_index=[]
        x = []
        y = []
        point_result=[]
        xlist,ylist,zlist,tlist=[],[],[],[]

        lines = self.pattern.split('\r\n')
        xlabel = re.split(r'\s{3,}',lines[0])[4]
        ylabel=re.split(r'\s{3,}',lines[0])[5]
        for line in lines[1:-1]:
            if line!='':
                cols=re.split(r'\s{3,}',line)
                x_index.append(cols[1])
                y_index.append(cols[2])
                x.append(cols[4])
                y.append(cols[5])
                point_result.append(cols[-2])

        x_cnt = len(self.remove_duplicates(x_index))
        print(x_cnt)

        xlist = self.remove_duplicates(x)
        ylist = self.remove_duplicates(y)
        tlist = self.split_list(point_result,x_cnt)
       # zlist = [[map(to_int, item) for item in sublist] for sublist in tlist]

        for sublist in tlist:
            zlist.append(list(map(to_int, sublist)))

        # print(zlist)

        return xlist,ylist,zlist,tlist,xlabel,ylabel
    def get_tname(self):
        name = re.findall('Test Name.*',self.head)[0]
        return name.replace('Test Name           ','')

    def remove_duplicates(self,lst):
        return [item for index, item in enumerate(lst) if item not in lst[:index]]

    def split_list(self, lst, chunk_size):
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]













if __name__== '__main__':
    with open('Serdes_SHM_detail.txt', 'r') as f:
        text = f.read()

    P = SHMViewer(text)
    patterns = P.match_pattern()
    for pattern in patterns:
        P.show_headfile(pattern)
        #P.plot_shm(pattern)

