from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time,re
from dotenv import load_dotenv
import os
load_dotenv()
url=os.environ["WEB_URL"]
forms=os.environ["FORM_LINK"]
main_data=requests.get(url=url)
data=main_data.text
soup=BeautifulSoup(data,'html.parser')
price=soup.find_all(name="span",class_="PropertyCardWrapper__StyledPriceLine")
address_tags = soup.find_all('address', {'data-test': 'property-card-addr'})
link_tags=soup.find_all(name='a',class_="StyledPropertyCardDataArea-anchor")
price_list=[]
for i in price:
    parts = re.split(r'(\$[\d,]+)', i.getText())
    s=''.join(part for part in parts if part.startswith('$') or (part.isdigit() and part))
    price_list.append(s)
address_list=[tag.get_text(strip=True) for tag in address_tags]
link_list=[tag.get('href') for tag in link_tags]


chromeOptions=webdriver.ChromeOptions()
chromeOptions.add_experimental_option('detach',True)
new_driver=webdriver.Chrome(options=chromeOptions)
for i in range(len(link_list)):
    new_driver.get(url=forms)
    address_column = new_driver.find_element(By.XPATH,
                                             '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')

    price_column = new_driver.find_element(By.XPATH,
                                           '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')


    link_column = new_driver.find_element(By.XPATH,
                                          '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    submit_button = new_driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    address_column.send_keys(address_list[i])
    price_column.send_keys(price_list[i])
    link_column.send_keys(link_list[i])
    time.sleep(1)
    submit_button.click()

