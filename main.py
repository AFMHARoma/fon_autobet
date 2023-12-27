import re
import time

import selenium.common.exceptions
import selenium.webdriver as wd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.expected_conditions as EC

FON_ESPORTS_LIVE_URL = 'https://fon.bet/live/esports'


class BetMachine:
    def __init__(self):
        self.match_data = None
        self.opts = Options()
        self.opts.add_argument("--user-data-dir=/UserDir")
        self.driver = wd.Chrome(options=self.opts)

    def __login(self):
        pass

    def __go_to_site(self):
        self.driver.get(FON_ESPORTS_LIVE_URL)
        rows_parent = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sport-section-virtual-list--6lYPYe')))
        time.sleep(5)
        self.rows_parent = rows_parent

    def __find_map_block(self):
        all_blocks = self.rows_parent.find_elements(By.XPATH, './div')[1:-1]
        for q, row in enumerate(all_blocks):
            try:
                match_name = row.find_element(By.XPATH, './div[3]/div[1]/a[1]').text
                if self.match_data['team1'] in match_name or self.match_data['team2'] in match_name:
                    for item in range(q + 1, q + 3):
                        if finder := re.search('\d-я карта', all_blocks[item].text):
                            if int(re.search('\d', finder[0])[0]) == self.match_data['map']:
                                self.map_row = all_blocks[item]
            except:
                pass

    def __select_bet(self):
        self.map_row.find_element(By.XPATH, f'./div[{4 + self.match_data["winner_ind"]}]').click()

    def __do_bet(self):
        try:
            coupon_info = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'new-coupon--5cY6lQ')))
            sum_input = coupon_info.find_element(By.TAG_NAME, 'input')
            sum_input.click()
            sum_input.send_keys(400)
        except selenium.common.exceptions.NoSuchElementException:
            self.__select_bet()
            self.__do_bet()
        bet_btn = self.driver.find_element(By.CLASS_NAME, 'button--9z8aUQ')
        while True:
            if 'disabled' not in bet_btn.get_attribute('innerHTML'):
                bet_btn.click()
                break
            else:
                if 'enabled' in (accept_btn := self.driver.find_element(By.CLASS_NAME, 'button-accept--5yxyi8')):
                    accept_btn.click()
            time.sleep(0.5)

    def do_bet(self, match_data):
        self.match_data = match_data
        self.__login()
        self.__go_to_site()
        self.__find_map_block()
        self.__select_bet()
        self.__do_bet()


def main():
    BetMachine().do_bet({'team1': 'Team Klee', 'team2': 'Klim Sani4', 'map': 4, 'winner_ind': 0})


if __name__ == '__main__':
    main()
