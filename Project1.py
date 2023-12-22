from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()
url = 'https://www.instahyre.com/python-jobs'
driver.maximize_window()
driver.get(url)
time.sleep(1)

data = []
total_entries = 320  # the project wants only greater than 300 data, so I took 320.
entries_per_page = 20
total_pages = total_entries // entries_per_page

for page in range(total_pages):
    old_height = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == old_height:
            break
        old_height = new_height

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="job-function-page"]/div[2]/div/div[1]/div[1]')))

    elements = driver.find_elements(By.XPATH, '//*[@id="job-function-page"]/div[2]/div/div[1]/div[1]/div')

    for idx, element in enumerate(elements, start=1):
        xpath_name = f'//*[@id="job-function-page"]/div[2]/div/div[1]/div[1]/div[{idx}]/div/div/div/div/div[2]/a/div[1]/div'
        xpath_loc = f'//*[@id="job-function-page"]/div[2]/div/div[1]/div[1]/div[{idx}]/div/div/div/div/div[2]/a/div[2]/span/span'
        xpath_founded = f'//*[@id="job-function-page"]/div[2]/div/div[1]/div[1]/div[{idx}]/div/div/div/div/div[2]/a/div[3]/span[1]/span'
        xpath_emp = f'//*[@id="job-function-page"]/div[2]/div/div[1]/div[1]/div[{idx}]/div/div/div/div/div[2]/a/div[3]/span[3]/span'
        xpath_about = f'//*[@id="job-function-page"]/div[2]/div/div[1]/div[1]/div[{idx}]/div/div/div/div/div[2]/a/div[4]'
        xpath_skills = f'//*[@id="job-function-page"]/div[2]/div/div[1]/div[1]/div[{idx}]/div/div/div/div/div[2]/a/div[5]/ul'
        xpath_link = f'/html/body/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[{idx}]/div/div/div/div/div[1]/a'

        try:
            ele1 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_name))).text
            ele2 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_loc))).text
            ele3 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_founded))).text
            ele4 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_emp))).text
            ele5 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_about))).text
            ele6 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_skills))).text
            link_element = driver.find_element(By.XPATH, value=xpath_link)
            link = link_element.get_attribute("href")
            
            data.append({
                'Name': ele1,
                'Location': ele2,
                'Founded': ele3,
                'Employee': ele4,
                'About': ele5,
                'Skills': ele6,
                'Link': link
            })
            if idx > 20:
                break

        except Exception as e:
            print(f"Error scraping data for job entry {idx} on page {page + 1}: {str(e)}")

    if page < total_pages - 1:
        next_page_xpath = '//*[@id="job-function-page"]/div[2]/div/div[1]/div[1]/div[21]/li[12]'
        try:
            next_page_button = driver.find_element(By.XPATH, next_page_xpath)
            next_page_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error navigating to the next page: {str(e)}")
            break

df = pd.DataFrame(data)
df.to_csv('Project_1_TRY.csv', index=False)

if 'driver' in locals():
    driver.quit()