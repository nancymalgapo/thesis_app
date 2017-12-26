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
from selenium.common.exceptions import NoSuchElementException

user = ""
pwd = ""

def login_user_trial(username, password):
    try:
        global user 
        global pwd
        user = username
        pwd = password
        browser = webdriver.Chrome()
        browser.set_window_position(0, 0)
        browser.get('https://www.plagscan.com/')
        userElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.left')))
        userElement.click()
        print('Finding username/password field ....')
        userElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'login_username')))
        username_field = browser.find_element_by_id('login_username')
        username_field.send_keys(user)
        password_field = browser.find_element_by_id('login_password')
        password_field.send_keys(pwd)
        sleep(5)  
        browser.find_element_by_id('loginBtnLaunch').click()
        print('hello')
        GoogleuserElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'identifierId')))
        google_username_field = browser.find_element_by_id('identifierId')
        google_username_field.send_keys(user)
        google_username_field_next = browser.find_element_by_id('identifierNext')
        google_username_field_next.click()
        sleep(2)
        GooglepwdElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'password')))
        google_password_field = browser.find_element_by_name('password')
        google_password_field.send_keys(pwd)
        google_password_field_next = browser.find_element_by_id('passwordNext')
        google_password_field_next.click()
        uploadElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'flashLink')))
        try:
            print('Signed In. Finding upload btn ...')
            sleep(5)
            uploadBtn = browser.find_element_by_xpath("//input[@id='fileInput']")
            browser.quit()
            return True
        except:
            browser.quit()
            print('Failed to login: Invalid Username and Password!')
            return False
    except NoSuchElementException:
        browser.quit()
        print('Failed to login: Check your internet connection!')
        return False

def plagscan_upload_trial(content):
    try:
        browser = webdriver.Chrome()
        browser.get('https://www.plagscan.com/')
        userElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.left')))
        userElement.click()
        print('Finding username/password field ....')
        userElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'login_username')))
        username_field = browser.find_element_by_id('login_username')
        username_field.send_keys(user)
        password_field = browser.find_element_by_id('login_password')
        password_field.send_keys(pwd)
        sleep(5)  
        browser.find_element_by_id('loginBtnLaunch').click()
        print('hello')
        GoogleuserElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'identifierId')))
        google_username_field = browser.find_element_by_id('identifierId')
        google_username_field.send_keys(user)
        google_username_field_next = browser.find_element_by_id('identifierNext')
        google_username_field_next.click()
        sleep(2)
        GooglepwdElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'password')))
        google_password_field = browser.find_element_by_name('password')
        sleep(2)
        google_password_field.send_keys(pwd)
        google_password_field_next = browser.find_element_by_id('passwordNext')
        google_password_field_next.click()
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
            return True
        except (NoSuchElementException, TimeoutException) as e :
            browser.quit()
            print('Failed to login: Invalid Username and Password!')
            return False
    except NoSuchElementException:
        print('Failed to login')
        browser.quit()
        return False