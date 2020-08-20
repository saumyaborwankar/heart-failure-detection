import requests
from bs4 import BeautifulSoup
import credentials
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
URL = 'https://yocket.in/applications-admits-rejects/465-university-of-washington/2'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
#results = soup.find()
mydivs = soup.findAll("div", {"class": "col-sm-6"})
'''
login_url = "https://yocket.in/account/login"
'''login_payload = {
    "email": credentials.email,
    "password": credentials.password
}'''
url_list = ['https://yocket.in/applications-admits-rejects/465-university-of-washington/2',
       'https://yocket.in/applications-admits-rejects/305-university-of-illinois-at-chicago/2'
       
       ]
for URL in url_list:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    names=[]
    profiles=[]
    periods=[]
    gres=[]
    eng=[]
    ug=[]
    exp=[]
    elements_in_page = soup.find_all("div", class_="col-sm-6")[2:]
    for element in elements_in_page:
        other_details = element.find_all("div", class_="col-sm-3")
        undergrad_details = other_details.__getitem__(3).get_text().split("\n").__getitem__(2).split(" ")
        name=("name", element.find_all("a").__getitem__(0).get_text().strip())
        profile=("profile_link", element.find_all("a").__getitem__(0).get("href").strip())
       
        period=("period", element.find_all("small").__getitem__(0).get_text().split("\n")[1:][1])
        gre=("gre", other_details.__getitem__(1).get_text().split("\n").__getitem__(2).strip())
        eng_test=("eng_test", other_details.__getitem__(2).get_text().split("\n").__getitem__(1).strip())
        eng_test_marks=("eng_test_marks", other_details.__getitem__(2).get_text().split("\n").__getitem__(2).strip())
        ug_marks=("undergrad_marks", undergrad_details.__getitem__(0).strip())
        score=("scoring", undergrad_details.__getitem__(1).strip())
        experience=("experience", other_details.__getitem__(4).get_text().split("\n").__getitem__(2).strip())
        names.append(name[1])
        profiles.append(profile[1])
        periods.append(period[1])
        gres.append(gre[1])
        eng.append(eng_test_marks[1])
        ug.append(ug_marks[1])
        exp.append(experience[1])
    import pandas as pd
    df=pd.DataFrame()
    df['names']=names
    df['profiles']=profiles
    df['periods']=periods
    df['gre']=gres
    df['TOEFL']=eng
    df['CGPA']=ug
    df['Experience']=exp
    
    uni_name=URL.split('/')[-2]
    
    df.to_csv('{}.csv'.format(uni_name))