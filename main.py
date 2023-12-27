import time

import selenium.webdriver as wd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

FON_ESPORTS_LIVE_URL = 'https://fon.bet/live/esports'


def login(driver):
    pass


def go_to_site(driver):
    driver.get(FON_ESPORTS_LIVE_URL)
    rows_parent = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sport-section-virtual-list--6lYPYe')))
    return rows_parent


def find_match(match_fon_block, match_data):
    for row in match_fon_block.find_elements(By.XPATH, './div')[1:-1]:
        try:
            match_name = row.find_element(By.XPATH, './div[3]/div[1]/a[1]').text
            if match_data['team1'] in match_name or match_data['team2'] in match_name:
                return row
        except:
            pass


def find_bet(driver):
    pass


def do_bet(driver):
    pass


def on_bet_error(driver, error):
    pass


def main():
    rows_parent = go_to_site(webdriver)
    match_row = find_match(rows_parent)



if __name__ == '__main__':
    webdriver = wd.Chrome()
    main()