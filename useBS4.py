from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen
import re
import numpy as np


doj_link="https://njdg.ecourts.gov.in/scnjdg/"
doj_link

doj_url=urlopen(doj_link)

doj_page=doj_url.read()

doj_html=bs(doj_page,"html.parser")
data=[]

with open("myscrappeddata.txt","a")as file:
    for i in range(11):
        box=doj_html.findAll("div",{"class":"card h-100"})[i].text
        # print(box)
        cleaned_text=re.sub('\s*\n\s*', '\n',box).strip()
        print(cleaned_text)
        file.write(cleaned_text+"\n")