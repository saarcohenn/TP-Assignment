import re
import sys
import time
from bs4 import BeautifulSoup
from  selenium import webdriver


def show_current_running_function(func):
    """
        Summary: The following method is a Decorator for showing the current 
                 running function
        input:   func -> reference to a function to
        output:  a wrapper_func that get's the original function call arguments
                 and return the the original return value
    """
    def wrapper_func(*args, **kwargs):
        # Do something before the function.
        print(f"<--- Starting {func.__name__} Function --->\n")
        ret_val = func(*args, **kwargs)
        # Do something after the function.
        print(f"\n<--- {func.__name__} Function Finished --->")
        return ret_val
    return wrapper_func

def get_site_url(input_url):
    """
        Summary: This method extracts the clean url (domain name and postfix)
        
        input:  input_url -> the original url page
        output: full_url -> the site domain url (clean url)
    """
    devided_url = re.split(r"/", input_url)
    full_url = "https://"
    for part in devided_url:
        if part != "https:" and part != "http:" and part != '':
            full_url += part + "/"
            break
    return full_url

def get_logo_url(page_source, url):
    """
        Summary: This method extract the logo url from a given site 
        
        input:  page_source -> the original page source
                url -> the original url page     
        output: logo_url -> The logo url
    """
    soup = BeautifulSoup(page_source, 'html.parser')
    img_elem = soup.find('img')
    logo_url = img_elem['src']

    if url not in logo_url and img_elem['src'].startswith("//"):
        logo_url = "https:" + logo_url
    elif url not in logo_url and img_elem['src'].startswith("/"):
        logo_url = url + logo_url
    return logo_url

def get_site_phones(page_source):
    """
        Summary: This method extract all phone numbers from a given site
        
        input:  page_source -> the original page source
        output: phones -> list of the founded phone numbers
    """
    phones = []
    soup = BeautifulSoup(page_source, 'html.parser')
    tags = soup.find_all(['p', 'span', 'a'])

    for tag in tags:
        match_phone = re.search(r"(\+)?(\d{1,3}\D{1,3})?(\(\d{1,3}\)|\d{1,3})(\D\d{2,4}){2,4}", tag.text)
        if match_phone:
            phoneNum = parsePhoneNumber(match_phone.group())
            if phoneNum not in phones:
                phones.append(phoneNum)
    return phones

def parsePhoneNumber(number):
    """
        Summary: This method light clean a given phone number

        input:  number -> original phone number
        output: new_number -> new and clean phone number
    """
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

def selenium_scrape(sites=None):
    """
        Summary: This method is in charge of the main loop of all the given websites.
                 It's purpose is to  get all the information needen and create a new dictionary 
                 which will contain the data and the print it as requested
        
        input:  sites -> a given list of websites
        output: new_number -> new and clean phone number
    """
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
            url = site.strip("\n")
            site_url = get_site_url(url)
            logo_url = get_logo_url(driver.page_source, site_url)
            phones_list = get_site_phones(driver.page_source)
            site_data = {
                "logo": logo_url,
                "phones": phones_list,
                "website": url
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

    # FOR STREAM
    for line in sys.stdin:
        sites.append(line.strip("\n"))

    # FOR DEBUG
    # with open("websites.txt") as f: 
        # sites = f.readlines() 
    
    print(sites)
    selenium_scrape(sites)
