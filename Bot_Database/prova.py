from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import urllib.request

browser = webdriver.Firefox()
def rates_fetcher(url):
    sada = browser.get(url)
    time.sleep(3)
    source = browser.page_source
    soup = BeautifulSoup(source, 'html.parser')
    for item in soup.findAll('div', attrs={'class': 'name'}):
        print(item.text)

url = "https://unaparolaalgiorno.it"
rates_fetcher(url)
