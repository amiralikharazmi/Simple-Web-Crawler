import jdatetime as jdatetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

NUMBER_OF_NEWS = 1000
SAVE_TO_FILE = 'data.csv'


def initial():
    chrome_options = Options()
    chrome_options.add_argument("webdriver.chrome.driver=driver/chromedriver.exe")
    global driver
    driver = webdriver.Chrome(options=chrome_options)


def get_link(category, date):
    start_url = f'https://www.irna.ir/page/archive.xhtml?&yr={date.year}&mn={date.month}&dy={date.day}'
    driver.get(start_url)

    select_category_xpath = '/html/body/main/section/div/div[1]/div/form/div[2]/div[1]/span'
    select_category = EC.presence_of_element_located((By.XPATH, select_category_xpath))
    WebDriverWait(driver, 50).until(select_category)
    select_category = driver.find_element(By.XPATH, select_category_xpath)
    select_category.click()

    input_category_xpath = '/html/body/span/span/span[1]/input'
    input_category = EC.presence_of_element_located((By.XPATH, select_category_xpath))
    WebDriverWait(driver, 50).until(input_category)
    input_category = driver.find_element(By.XPATH, input_category_xpath)
    if category == 'sport':
        input_category.send_keys('ورزش')
    elif category == 'economy':
        input_category.send_keys('اقتصاد')
    elif category == 'politic':
        input_category.send_keys('سیاست')
    else:
        return 'Wrong Category!!'
    sport_category_xpath = '/html/body/span/span/span[2]/ul'
    select_category_ul = EC.presence_of_element_located((By.XPATH, select_category_xpath))
    WebDriverWait(driver, 50).until(select_category_ul)
    select_category_ul = driver.find_element(By.XPATH, sport_category_xpath)
    select_category_ul.find_elements(By.TAG_NAME, 'li')[0].click()


def next_page():
    pagination_ul_xpath = "/html/body/main/section/div/div[2]/div[1]/section/footer/div/ul"
    pagination_ul = EC.presence_of_element_located((By.XPATH, pagination_ul_xpath))
    WebDriverWait(driver, 50).until(pagination_ul)
    pagination_ul = driver.find_element(By.XPATH, pagination_ul_xpath)
    pagination_li = pagination_ul.find_elements(By.TAG_NAME, 'li')
    pagination_li[-1].click()  # next page


def start_crawl(category, save_to, ):
    date = jdatetime.date(year=1402, month=6, day=8)  # last date
    get_link(category=category, date=date)
    count = 0
    with open(save_to, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Text', 'Category'])
        while count < NUMBER_OF_NEWS:

            news_ul_xpath = "/html/body/main/section/div/div[2]/div[1]/section/div/ul"
            news_ul = EC.presence_of_element_located((By.XPATH, news_ul_xpath))
            WebDriverWait(driver, 50).until(news_ul)
            news_ul = driver.find_element(By.XPATH, news_ul_xpath)
            news_li = news_ul.find_elements(By.TAG_NAME, 'li')

            for li in news_li:
                text = li.text.split('\n')[0]
                csv_writer.writerow([text, category])
                count += 1
                if count < NUMBER_OF_NEWS:
                    pass
                else:
                    driver.quit()
                    return
            next_page()
    driver.quit()


categories = ['sport', 'politic', 'economy']
for cate in categories:
    print(f'Crawling {cate} news...')
    initial()
    start_crawl(category=cate, save_to=SAVE_TO_FILE)

print(f'{NUMBER_OF_NEWS} news crawled!')
