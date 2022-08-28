# -*- coding: utf-8 -*-  
import requests
from bs4 import BeautifulSoup
import time
from urllib.request import urlopen
from urllib.parse import quote
import xlwt
interval=3      #请求间隔

def save_file(row):
    for i in range(len(row)):
        shell1.write(index,i,row[i])
        
def get_info(bs):
    videos=bs.find_all('li',{'class':'video-item'})
    global index
    for v in videos:
        index+=1
        info=v.find('div',class_='info')
        vtype=info.find('span','type hide').text.strip()
        title=info.find('a','title')['title'].strip()
        watch_num=info.find('span','watch-num').text.strip()
        p_time=info.find('span','so-icon time').text.strip()
        danmu=info.find('span','so-icon hide').text.strip()
        up_name=info.find('a','up-name').text.strip()
        t_long=v.select_one('a:nth-child(1) > div:nth-child(1) > span:nth-child(2)').text.strip()
        save_file((str(index),title,up_name,vtype,t_long, p_time,watch_num,danmu)) 
        
if __name__ == '__main__':
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'}
    index=0
    f=xlwt.Workbook()
    shell1=f.add_sheet('bilibili')
    row0=('id','标题','up主','类型','时长','上传时间','观看量','弹幕数')
    for i in range(len(row0)):
        shell1.write(0,i,row0[i])    
    base_url="https://search.bilibili.com/all?keyword="
    name=quote(input("请输入需要查找的关键字:\n"))
    url=base_url+name
    res=requests.get(url,headers=headers)
    bs=BeautifulSoup(res.text,'lxml')
    try:
        pages=bs.find_all('button',{'class': 'pagination-btn'})[-1].text.strip()
    except:
        print("未找到相应内容!!!")
        exit(1)
    print("共找到"+pages+"页内容\n正在爬取第1页视频信息...")
    get_info(bs)
    suffix=str(time.time()).split('.')[0]
    f.save('bilibili_'+suffix+'.xls')       #实时保存    
    for i in range(1,int(pages)+1):
        time.sleep(interval)
        print("正在爬取第"+str(i)+"页视频信息...")
        url2=url+'&page='+str(i)   
        res=requests.get(url2,headers=headers)
        bs=BeautifulSoup(res.text,'lxml')
        get_info(bs)
        f.save('bilibili_'+suffix+'.xls')       #实时保存
    
    
    
    