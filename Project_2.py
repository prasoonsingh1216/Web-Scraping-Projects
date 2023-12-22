from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()

all_data = []  # To store data across all seasons

for i in range(2008, 2024):
    driver.get(f'https://www.iplt20.com/matches/results/{i}')
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)

    elements = driver.find_elements(By.XPATH, '//*[@id="team_archive"]/li')

    data = []
    wait = WebDriverWait(driver, 10)

    for idx, element in enumerate(elements, start=1):
        xpath_session = f'//*[@id="smResultsWidget"]/div/div[1]/div/div[1]/div/div[4]/div/div[1]'
        xpath_match_no = f'//*[@id="team_archive"]/li[{idx}]/div[1]/div[1]/span[1]'
        xpath_venue = f'//*[@id="team_archive"]/li[{idx}]/div[1]/div[2]/span/p/span'
        xpath_DT = f'//*[@id="team_archive"]/li[{idx}]/div[1]/div[2]/div'
        xpath_win = f'//*[@id="team_archive"]/li[{idx}]/div[2]/div[1]/div'
        xpath_first = f'//*[@id="team_archive"]/li[{idx}]/div[2]/div[2]/div/div[1]/div'
        xpath_second = f'//*[@id="team_archive"]/li[{idx}]/div[2]/div[2]/div/div[2]/div'
        xpath_link = f'//*[@id="team_archive"]/li[{idx}]/div[2]/div[3]/div/a'

        try:
            ele1 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_session))).text
            ele2 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_match_no))).text
            ele3 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_venue))).text
            ele4 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_DT))).text
            ele5 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_win))).text
            ele6 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_first))).text
            ele7 = wait.until(EC.presence_of_element_located((By.XPATH, xpath_second))).text
            link_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_link)))
            link = link_element.get_attribute("href")

            data.append({
                'Season': i,
                'Session': ele1,
                'Match Number': ele2,
                'Venue': ele3,
                'Date and Time': ele4,
                'Winner': ele5,
                'First Team': ele6,
                'Second Team': ele7,
                'Link': link
            })
        except Exception as e:
            print(f"Error scraping data for match {i}-{idx}: {e}")

    all_data.extend(data)

df = pd.DataFrame(all_data)
df.to_csv('Project_2_output.csv', index=False)

if 'driver' in locals():
    driver.quit()
