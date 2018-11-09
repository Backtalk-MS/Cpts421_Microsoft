import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import datetime
import time

def wait_for(condition_function):
    start_time = time.time() 
    while time.time() < start_time + 3: 
        if condition_function(): 
            return True 
        else: 
            time.sleep(0.1) 
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__) 
    )

def click_button_by_id_present_element(id):
    link = driver.find_element_by_id(id)
    threads = driver.find_element_by_id("threads")
    link.click()
    def ref_has_gone_stale():
        try:
            threads.find_elements_by_xpath('.//data-bi-id') 
            return False
        except StaleElementReferenceException:
            return True
    wait_for(ref_has_gone_stale)

def click_button_by_id_new_element(id):
    link = driver.find_element_by_id(id)
    link.click()
    try:
        elem = WebDriverWait(driver,10).until(
            expected_conditions.presence_of_element_located((By.ID,"pagerBottom"))
        )
        return elem
    except TimeoutException:
        print("WebDriverWait Time Out waiting for element presence by ID")

def date_generator(start, end):
    for ord in range(start.toordinal(), end.toordinal()):
        yield datetime.date.fromordinal(ord)

def get_forum_links_from_webpage_on_dates(url, driver, posted_after_date, posted_before_date):
    driver.get(url)
    posted_after_field = driver.find_element_by_id("postedAfter")
    posted_after_field.clear()
    posted_after_field.send_keys(posted_after_date)
    posted_after_field.send_keys(Keys.ENTER)
    posted_before_field = driver.find_element_by_id("postedBefore")
    posted_before_field.clear()
    posted_before_field.send_keys(posted_before_date)
    posted_before_field.send_keys(Keys.ENTER)
    try:
        click_button_by_id_present_element("applyButton")
    except:
        click_button_by_id_present_element("applyButton")
    links = []
    xpath_search_element = ".//a[@data-bi-id='thread-link']"
    try:
        links = driver.find_element_by_id("threads").find_elements_by_xpath(xpath_search_element)
    except NoSuchElementException:
        print("Could not element of the form: {}".format(xpath_search_element))

    if links is None or len(links) == 0:
        return []
    else: 
        return [el.get_attribute("href") for el in links]

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(30)
main_category = sys.argv[1]
sub_category = sys.argv[2]

url="https://answers.microsoft.com/en-us/{}/forum/{}?sort=CreatedDate&dir=Asc&tab=Threads&status=all&mod=&modAge=&advFil=&postedAfter=2014-10-12&postedBefore=2014-10-13&threadType=questions&isFilterExpanded=true&page=1".format(main_category,sub_category)

start_date = datetime.date(int(sys.argv[6]),int(sys.argv[4]),int(sys.argv[5]))
end_date = datetime.date(2018,11,7)
var_date = end_date

f=open("MS_Answers_{}_{}.txt".format(main_category,sub_category),'w',encoding='utf-8')

day_delta = int(sys.argv[3])

total_elements_found = 0
sequential_failures = 0

while var_date > start_date:
    # print(var_date)
    next_day = var_date - datetime.timedelta(days=day_delta)
    if next_day < start_date:
        next_day = start_date
    links = get_forum_links_from_webpage_on_dates(url,driver,"{}/{}/{}".format(next_day.month,next_day.day,next_day.year),"{}/{}/{}".format(var_date.month,var_date.day,var_date.year))
    if len(links) == 0:
        day_delta*=2
        sequential_failures+=1
    else:
        if day_delta > 1:
            day_delta-=1
        sequential_failures = 0
        for link in links:
            f.write(link+'\n')
    var_date = next_day
    total_elements_found += len(links)
    print("{}:{} === day: {}, day_delta: {}, sequential failures: {}, total elements found: {}".format(main_category,sub_category,var_date,day_delta, sequential_failures, total_elements_found))
    if sequential_failures >= 8:
        print("Exceeded failure tolerance")
        break
f.close()

# close the browser window
driver.quit()