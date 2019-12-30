from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import time
import csv
from datetime import date
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome('./chromedriver',options=chrome_options)
# driver = webdriver.Chrome()
starting_url = 'https://www.hotstar.com/us/channels'
wait = WebDriverWait(driver, 120)
# driver.minimize_window()


index=1

def channel_list_extractor(driver,channel_name,channel_link):
    driver.get(starting_url)
    scroller(driver,2)
    wait.until(EC.presence_of_element_located((By.XPATH, """//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/div/div/div/div[1]/div""")))
    soup= BeautifulSoup(driver.page_source)
    channel_div = soup.find('div',class_='resClass')
    channel_no = channel_div.find_all('div',class_='normal')
    global index
    for x in channel_no:
        l=x.find('a',href=True)
        name=l['href'].split('/')[3]
        channel_name.append(name)
        l='https://www.hotstar.com'+l['href']
        # csv_writer.writerow([str(index),name])
        # index=index+1
        channel_link.append(l)





def show_name_extractor(driver,url,channel_name,show_name,csv_writer):
    global index
    today = date.today()

    driver.get(url)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, """//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/div/div/div/div[1]/div""")))

    scroller(driver,2)
    soup = BeautifulSoup(driver.page_source)
    show_div = soup.find('div',class_='resClass')
    show_no = show_div.find_all('div',class_='normal')
    for x in show_no:
        l=x.find('a',href=True)
        name=l['href'].split('/')[3]
        # l=str(l)
        # l=l.strip()
        # l=l.replace(' ','-')
        # l=l.replace('.','')
        # print(l)
        show_name.append(name)
        csv_writer.writerow([str(index),str(channel_name),str(name.lower()),str(today)])
        index=index+1

def scroller(driver, pause):
    time.sleep(pause)
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(pause)
            newHeight = driver.execute_script("return document.body.scrollHeight")

            if (newHeight == lastHeight):
                break

            lastHeight = newHeight
        except NoSuchElementException as e:
            print("Done Scrolling!")

def runner():
    csv_file = open('hotstar_data1.csv', 'w', encoding="utf-8")
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['index', 'channel_name', 'show_name','date-added'])
    # csv_writer.writerow(['index', 'ch'])

    global index
    index=1

    with open('show_name.txt','r') as r:
        z=r.read()
        show_name_bk= z.split()


    with open('channel_name.txt','r') as r:
        z=r.read()
        channel_name_bk= z.split()

    channel_link = []
    channel_name = []
    show_name = []
    print('\nStarted Extracting!!! Please Wait....\n')

    channel_list_extractor(driver,channel_name,channel_link)
    for z in range(len(channel_link)):
        show_name_extractor(driver,channel_link[z],channel_name[z],show_name,csv_writer)

    print('\n\nDONE\n\n')
    # print(channel_name)

    if len(set(channel_name).difference(channel_name_bk))==0:
        print('no new channels')
    else:
        print('Newly added channel : ',end=' ')
        print(set(channel_name).difference(channel_name_bk))


    if len(set(show_name).difference(show_name_bk))==0:
        print('no new shows')
    else:
        print('Newly added shows : ',end=' ')
        print(set(show_name).difference(show_name_bk))


    with open('channel_name.txt','w',encoding="utf-8") as w:
        for l in channel_name:
            w.write(l)
            w.write('\n')
    print('\n\n')
    with open('show_name.txt','w',encoding="utf-8") as w:
        for l in show_name:
            w.write(l)
            w.write('\n')

    csv_file.close()



while True:
    runner()
    time.sleep(72000)
