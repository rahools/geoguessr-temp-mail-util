import requests
import random
import string
import time
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

API = 'https://www.1secmail.com/api/v1/'
GEOGUESSR = 'https://www.geoguessr.com/signup'
PASSWD = 'Bittu@1234'
domainList = ['1secmail.com', '1secmail.net', '1secmail.org']
domain = random.choice(domainList)


def generateUserName():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))

    return username

def extract():
    getUserName = re.search(r'login=(.*)&',newMail).group(1)
    getDomain = re.search(r'domain=(.*)', newMail).group(1)

    return [getUserName, getDomain]

def findUrls(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)    

    return [x[0] for x in url]

def checkMails():
    reqLink = f'{API}?action=getMessages&login={extract()[0]}&domain={extract()[1]}'
    req = requests.get(reqLink).json()
    length = len(req)
    if length == 0:
        pass
    else:
        idList = []
        for i in req:
            for k,v in i.items():
                if k == 'id':
                    mailId = v
                    idList.append(mailId)

        x = 'mails' if length > 1 else 'mail'

        for i in idList:
            msgRead = f'{API}?action=readMessage&login={extract()[0]}&domain={extract()[1]}&id={i}'
            req = requests.get(msgRead).json()
            for k,v in req.items():
                if k == 'body':
                    sender = v

            for i in findUrls(str(sender)):
                if 'https://www.geoguessr.com/profile/set-password/' in i:
                    return i

    return None


if __name__ == '__main__':
    # request new email
    newMail = f"{API}?login={generateUserName()}&domain={domain}"
    reqMail = requests.get(newMail)
    mail = f"{extract()[0]}@{extract()[1]}"
    print(f'Mail: {mail}')

    # signup on geoguessr
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(GEOGUESSR)
    elem = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div/div/div/form/div/div[1]/div[2]/input")
    elem.send_keys(mail)
    elem.send_keys(Keys.RETURN)

    # get & open registration email
    reset_url = None
    while reset_url == None:
        reset_url = checkMails()
        time.sleep(5)
    print(f'Reg Link: {reset_url}')
    driver.get(reset_url)

    # set password
    elem = driver.find_element_by_xpath("/html/body/div/div/main/form/section/section[2]/div/div[1]/div[2]/input")
    elem.send_keys(PASSWD)
    elem = driver.find_element_by_xpath("/html/body/div/div/main/form/section/section[2]/div/div[2]/div[2]/input")
    elem.send_keys(PASSWD)
    elem.send_keys(Keys.RETURN)

    # navigate to homepage
    elem = driver.find_element_by_xpath("/html/body/div/div/aside/div/ul[1]/li[3]/a")
    elem.click()
    time.sleep(2)

    # avoid race condition
    driver.refresh()
    time.sleep(1)

    # navigate to country streak
    elem = driver.find_element_by_xpath("/html/body/div/div/main/div/div/div[2]/section/section[1]/div/div/div[2]/div/a")
    elem.click()
    time.sleep(1)

    # start country streak
    elem = driver.find_element_by_xpath("/html/body/div/div/main/div/div/div/div/div/div/div[2]/article/div[4]/button")
    elem.click()
    time.sleep(1)
    
    # start country streak
    elem = driver.find_element_by_xpath("/html/body/div/section/div/div[2]/button[1]")
    elem.click()

