import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
import re
        
def wait_time():
    t_random = random.random()
    t = random.randint(1,3)
    t_sleep = t + t_random
    print(f"Sleep for {t_sleep} seconds")
    time.sleep(t_sleep)

def scrape_site(COMPANY):
    
    company = COMPANY
    sample_url = f'https://www.reclameaqui.com.br/empresa/{company}/lista-reclamacoes/?pagina=1'   
    base_url = 'https://www.reclameaqui.com.br/empresa'
    
    data = []
    print(f"Begin extraction of {sample_url}")
    options = webdriver.ChromeOptions()
    #options.headless = True

    #options.add_argument("window-size=1920x1080")
    #options.add_argument('--no-sandbox')
    #options.add_argument('--disable-gpu')

    # options.add_argument('--disable-dev-shm-usage') # Not used 
    driver = webdriver.Chrome(options=options)
    
    driver.get(sample_url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    complains = soup.find_all("ul", {"class": "complain-list"})
    complains = complains[0]
    links = complains.findAll('a', attrs={'href': re.compile(f"/{company}/")})
    
    l = links[0]
    
    for l in links:
        output = {}

        url_pro = l.get('href')
        
        driver.get(base_url+url_pro)
        
        html_complain = driver.page_source
        soup_complaint = BeautifulSoup(html_complain, 'html.parser')
        
        #Date
        complaint_info = soup_complaint.findAll('ul', attrs={'class': 'local-date'})
        complaint_info = complaint_info[0].findAll('li')
        
        data_location = complaint_info[0].text
        data_id = complaint_info[1].text
        data_time = complaint_info[2].text
        
        #Description
        complaint_description = soup_complaint.findAll('div', attrs={'class': 'complain-body'})
        complaint_description = complaint_description[0].find('p')
        data_description = complaint_description.text
        
        output['id'] = data_id
        output['date'] = data_time
        output['location'] = data_location
        output['complaint'] = data_description
        
        data.append(output)
        
        wait_time()
            
    driver.close()

    print(f"End extraction of {sample_url}")
    
    df = pd.DataFrame(data)
    df.to_csv('results.csv', index=False)
    return df

scrape_site(COMPANY)