import re
import sys
import time
from bs4 import BeautifulSoup
from  selenium import webdriver

def running_function(func):

    def wrapper_func(*args, **kwargs):
        # Do something before the function.
        print(f"<--- Starting {func.__name__} Function --->\n")
        ret_val = func(*args, **kwargs)
        # Do something after the function.
        print(f"\n<--- {func.__name__} Function Finished --->")
        return ret_val
    return wrapper_func

@running_function
def get_site_url(site_name):
    devided_url = re.split(r"/", site_name)
    
    full_url = "https://"
    for part in devided_url:
        if part != "https:" and part != "http:" and part != '':
            full_url += part + "/"
            break
    print(full_url)
    return full_url

@running_function
def get_logo_url(page_source, url):
    soup = BeautifulSoup(page_source, 'html.parser')
    img_elem = soup.find('img')
    src_url = img_elem['src']

    if url not in src_url and img_elem['src'].startswith("//"):
        src_url = "https:" + src_url
    elif url not in src_url and img_elem['src'].startswith("/"):
        src_url = url + src_url

    print("Logo URL:", src_url)
    return src_url

@running_function
def get_site_phones(page_source):
    phones = []
    soup = BeautifulSoup(page_source, 'html.parser')
    p_elems = soup.find_all('p')

    for p in p_elems:
        # re_phone = re.findall(r"(\+)?(\(\d{1,3}\)|\d{1,3})(\D\d{2,4}){2,3}", p.text)
        re_phone = re.search(r"(\+)?(\(\d{1,3}\)|\d{1,3})(\D\d{2,4}){2,3}", p.text)
        if re_phone:
            print(re_phone.group())
            phones.append(parsePhoneNumber(re_phone.group()))
    print(phones)

def parsePhoneNumber(number):
    if not number.startswith("+"):
        number = "+" + number

    allowed = "+ ()0123456789"
    new_number = ''
    for c in number:
        if c in allowed:
            new_number += c
        else:
            new_number += ' '
    return new_number

@running_function
def selenium_scrape(sites=None):
    chromedriver_path = "./chromedriver"
    driver = webdriver.Chrome(executable_path=chromedriver_path)
    try:
        i = 1
        for site in sites:
            if i != 1:
                # opens in a new browser tab
                driver.execute_script(f"window.open('about:blank', '{i}tab');")
                # It is switching to second tab now
                driver.switch_to.window(f"{i}tab")

            driver.get(site)
            url = get_site_url(site)
            logo_url = get_logo_url(driver.page_source, url)
            phones_list = get_site_phones(driver.page_source)
            site_data = {
                "logo": logo_url,
                "phones": phones_list,
                "website": site
            }
            print(site_data)
            time.sleep(1)
            i += 1
    except Exception as e:
        print(e)
    finally:
        # close driver
        driver.close()

def welcome_message():
    message = "Hello Trusted Partners"
    print("\n")
    print("*" * len(message))
    print(message)
    print("*" * len(message))
    print("\n")

if __name__ == '__main__':
    welcome_message()
    sites = []
    for line in sys.stdin:
        sites.append(line.strip("\n"))

    # with open("websites.txt") as f: 
    #     sites = f.readlines() 
    
    print(sites)
    selenium_scrape(sites)
