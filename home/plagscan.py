from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import pdb
import os
from os.path import dirname, realpath
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from .plagscan_trial import login_user_trial, plagscan_upload_trial

user = ""
pwd = ""

def login_user(username, password):
    try:
        global user 
        global pwd
        user = username
        pwd = password
        browser = webdriver.Chrome()
        browser.set_window_position(0, 0)
        browser.get('https://www.plagscan.com/pup')
        # fill in username and hit the next button
        sleep(2)
        print('Finding username/password field ....')
        userElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'UserEmail')))
        username_field = browser.find_element_by_id('UserEmail')
        username_field.send_keys(username)
        password_field = browser.find_element_by_id('UserPass')
        password_field.send_keys(password)
        signInButton = browser.find_element_by_id('btn-login')
        signInButton.click()
        sleep(5)
        try:
            print('Signed In. Finding upload btn ...')
            sleep(5)
            uploadBtn = browser.find_element_by_xpath("//input[@id='fileInput']")
            browser.quit()
            return True
        except TimeoutException:
            browser.quit()
            print('TimeoutException')
            return False
        except:
            print('Trial Account')
            browser.quit()
            if login_user_trial(username, password):
                return True
            else:
                messages.warning(
                    request, 'Login failed! Please enter a valid username and password, or check your internet connection and try again!')
                return False
    except:
        return False

def plagscan_upload(content):
    try:
        browser = webdriver.Chrome()
        browser.get('https://www.plagscan.com/pup')
        print('Finding username/password field ....')
        userElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'UserEmail')))
        username_field = browser.find_element_by_id('UserEmail')
        username_field.send_keys(user)
        password_field = browser.find_element_by_id('UserPass')
        password_field.send_keys(pwd)
        sleep(5)
        browser.find_element_by_id('btn-login').click()
        print('hello')
        uploadElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'flashLink')))
        try:
            print('Signed In.')
            uploadBtn = browser.find_element_by_xpath("//input[@id='fileInput']")
            print('Found Upload Button')
            uploadBtn.send_keys(content)
            print('Clicked Upload Button')
            sleep(5)
            process = WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'fa-circle-o-notch')))
            print('DONE')
            sleep(2)
            checkBtnElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn.btn-block.btn-sm.btn-default')))
            checkBtn = browser.find_element_by_xpath("//tbody[@id='newUploads']//a[@class='btn btn-block btn-sm btn-default']")
            checkBtn.click()
            # TRY AND EXCEPT FOR RESULT
            return True
        except TimeoutException:
            print('ito na')
            browser.quit()
            print('Timeout Exception')
            return False
        except NoSuchElementException:
            browser.quit()
            print('NoSuchElementException')
            return False
    except:
        browser.quit()
        if plagscan_upload_trial(content):
            return True
        else:
            messages.warning(
                request, 'Login failed! Please enter a valid username and password, or check your internet connection and try again!')
            return False
