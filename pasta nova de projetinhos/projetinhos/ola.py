from bs4 import BeautifulSoup as bs
import requests
import time
import pyautogui


def bot_spam(url, tag):
     time.sleep(5)
     req= requests.get(url)
     parse = bs(req.text, 'html.parser')
     print(parse)

bot_spam('https://vg.abaco.com.br/transparencia/servlet/wmservidores?0', '')