#!/usr/bin/env python
# coding: utf-8
from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
import re
class Get_Inputs:
    
    def inputs(locations):
        
        parameter=[]
        for i in locations:
            S=HTMLSession()
            query=i
            url=f'https://www.google.com/search?q=weather+{query}'
            r=S.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'})
            Parameters=[]
            Temperature=r.html.find('span#wob_tm',first=True).text
            Unit=r.html.find('div.vk_bk.wob-unit span.wob_t',first=True).text
            Prob_Rain=r.html.find('span#wob_pp',first=True).text
            i=i.lower()
            page = requests.get(f'https://www.worldweatheronline.com/{i}-weather/west-midlands/gb.aspx')
            soup = BeautifulSoup(page.text, 'html.parser')
            table=soup.find(class_='ws-details-item')
            mydivs = soup.findAll("div", {"class": "ws-details-item"})
            lines = [span.get_text() for span in mydivs]
            Rain=re.findall("\d+\.\d+", lines[1])
            Rain=float(Rain[0])
            Relative_Humidity=r.html.find('span#wob_hm',first=True).text
            Wind=r.html.find('span#wob_ws',first=True).text
            Parameters=[]
            Parameters.append(Temperature)
            Parameters.append(Relative_Humidity)
            Parameters.append(Wind)
            Parameters.append(Prob_Rain)
            new_parameters=[]
            for x in Parameters:
                res = ''.join(i for i in x if i.isdigit())
                new_parameters.append(float(res))
            new_parameters.insert(1,Rain)
            parameter.append(new_parameters)
            
        return parameter
    