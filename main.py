import platform
import re
import sys
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
        self.opts.add_argument(f"--user-data-dir={'/' if sys.platform == 'win32' else '.'}/UserDir")
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
        all_blocks = self.rows_parent.find_elements(By.XPATH, './div')[1:]
        for q, row in enumerate(all_blocks):
            try:
                match_name = row.find_element(By.XPATH, './div[3]/div[1]/a').text
                print(match_name)
                if self.match_data['team1'] in match_name and self.match_data['team2'] in match_name:
                    for item in range(q, q + 3):
                        if finder := re.search('\d-я карта', all_blocks[item].text):
                            if int(re.search('\d', finder[0])[0]) == self.match_data['map']:
                                self.map_row = all_blocks[item]
                                return
            except:
                pass
        print('Матча нет в линии')
        raise NotImplementedError

    def __select_bet(self):
        bet_cell = self.map_row.find_element(By.XPATH, f'./div[{4 + self.match_data["winner_ind"]}]')
        if 'value-state-empty--5jICeJ' not in bet_cell.get_attribute('class'):
            bet_cell.click()
        else:
            print('Котировок нет')
            raise NotImplementedError

    def __do_bet(self):
        try:
            self.coupon_info = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'new-coupon--5cY6lQ')))
            sum_input = self.coupon_info.find_element(By.TAG_NAME, 'input')
            sum_input.click()
        except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.TimeoutException):
            self.__select_bet()
            self.__do_bet()
            return

        stake_elements = self.coupon_info.find_elements(By.CLASS_NAME, 'info-block__value--7qWjdR')
        try:
            min_stake, max_stake = map(int, [stake_elements[1].text, stake_elements[2].text])
        except IndexError:
            print('Ставка недоступна')
            raise NotImplementedError

        sum_input.clear()
        sum_input.send_keys(max_stake)

        bet_btn = self.driver.find_element(By.CLASS_NAME, 'button--9z8aUQ')
        while True:
            if 'disabled' not in bet_btn.get_attribute('class'):
                bet_btn.click()
                break
            else:
                if 'enabled' in (accept_btn := self.driver.find_element(By.CLASS_NAME, 'button-accept--5yxyi8')).get_attribute('class'):
                    accept_btn.click()
            time.sleep(0.5)

    def __assure_bet(self):
        time.sleep(1)

        try:
            if self.driver.find_element(By.CLASS_NAME, '_no-funds'):
                print('Недостаточно средств')
                raise NotImplementedError
        except selenium.common.exceptions.NoSuchElementException:
            pass

        try:
            self.coupon_info.find_element(By.CLASS_NAME, 'seconds-overlay--2hF2If')
        except selenium.common.exceptions.NoSuchElementException:
            print('Прием ставки не начался')
            raise NotImplementedError

        try:
            while self.coupon_info.find_element(By.CLASS_NAME, 'seconds-overlay--2hF2If'):
                pass
        except selenium.common.exceptions.NoSuchElementException:
            pass

        try:
            if self.coupon_info.find_element(By.CLASS_NAME, 'error-box--6JzFgX'):
                self.coupon_info.find_element(By.CLASS_NAME, 'button-area--3vJ6vJ').click()
                time.sleep(60)
                self.__do_bet()
        except selenium.common.exceptions.NoSuchElementException:
            print('Ставка принята')

    def do_bet(self, match_data):
        try:
            self.match_data = match_data
            self.__login()
            self.__go_to_site()
            self.__find_map_block()
            self.__select_bet()
            self.__do_bet()
            self.__assure_bet()
        except NotImplementedError:
            pass


def main():
    bm = BetMachine()
    bm.do_bet({'team1': 'Purple haze', 'team2': 'Gameinside', 'map': 1, 'winner_ind': 0})


if __name__ == '__main__':
    print(sys.platform)
    main()
