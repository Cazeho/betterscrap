import streamlit as st
import os.path
from PIL import Image
import time
import requests as rq
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from seleniumwire import webdriver as wire_driver
from seleniumwire.thirdparty.mitmproxy.exceptions import TcpException
import logging
import json

IMAGE="image"

if os.path.isdir(IMAGE) == False:
    path = os.path.join(os.getcwd(), IMAGE)
    os.mkdir(path)

LOG_FILENAME = './onion.out'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

#logging.debug('This message should go to the log file')

seleniumwire_options = {
    'verify_ssl': False,
    'suppress_connection_errors': False   # Bypass SSL verification
}


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
driver = wire_driver.Chrome(seleniumwire_options=seleniumwire_options,options=options)




               
# https://api.mnemonic.no/pdns/v3/fr.zone-secure.net
def parse_dns(url):
     pass

def scan(url):
    del driver.requests
    try:
        driver.get(url)
        u=url.replace('https://','').replace('/','')
        time.sleep(5)
        img=u+".png"
        driver.save_screenshot(IMAGE+"/"+img)
        a=IMAGE+"/"+img
        b=[]
        c=[]
       
        for request in driver.requests:
                b.append(request.url)
                c.append(str(request.body))
        
        main={}
        l=[]

        for i,k in zip(b,c):
             data={}
             data["url"]=i
             data["body"]=k
             l.append(data)
             del data
        driver.close()
        main["data"]=l
        return a,main
    except Exception as e:
        logging.error(e, exc_info=True)
        raise

# https://utilimixfr.com


# https://github.com/hampusborgos/country-flags/blob/main/countries.json

st.title("Betterscrap")


"""
from streamlit_tags import st_tags



with st.form(key='scan'):
    multi_u = st_tags(
    label='### search urls to analyse:',
    text='Press enter to add more',
    maxtags = 10,
    key='1')
    #u= st.text_input("Scan url")
    submit = st.form_submit_button(label='Analyse')





if submit:
     st.write(multi_u)


"""


import json
import re

def search_in_json(json_input, result=[]):
    if isinstance(json_input, dict):
        for key, value in json_input.items():
            if isinstance(value, (dict, list, str)):
                search_in_json(value,result)
    elif isinstance(json_input, list):
        for item in json_input:
            if isinstance(item, (dict, list, str)):
                search_in_json(item,result)
    elif isinstance(json_input, str):
        matches = re.findall(r"\b[a-zA-Z0-9\-]*\.onion\b", json_input)
        result.extend(matches)
        for match in matches:
            st.write(match)
    return result






with st.form(key='scan'):
    u= st.text_input("Scan url")
    submit = st.form_submit_button(label='Analyse')


if submit and u != "":
    start = time.time()
    a,data=scan(u)
    q=search_in_json(data)
    st.write(q)
    image=Image.open(a)

    col1, col2 = st.columns(2)
    col1.metric("Requests", len(data["data"]))
    col2.metric("Onion url", len(q))




    st.write(data)
    st.image(image, caption='Screenshot')
    end = time.time()
    total_time = end - start
    st.write("Execution time: ",total_time)





