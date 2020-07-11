from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import validators

# import configs
from config import *

#web browser driver
driver = webdriver.Chrome('D:\whatsapp\chromedriver')
whatsapp_web_url = "https://api.WhatsApp.com/send?phone="

'''
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
'''

def authenticate():
    driver.get("https://web.whatsapp.com/")
    # wait = WebDriverWait(driver, 180)
    wait = WebDriverWait(driver, 180).until(ec.presence_of_element_located((By.CLASS_NAME, '_1kdBg')))


def sendMessage(whatsappMessage):
    # sending messages
    wait = WebDriverWait(driver, 180).until(ec.presence_of_element_located((By.CLASS_NAME, '_3uMse')))
    input_box = driver.find_element_by_class_name('_3uMse')
    # time.sleep(2)
    for eachMessage in whatsappMessage.split('\n'):
        while True:
            input_box.send_keys(eachMessage)
            # time.sleep(2)
            if input_box.text == eachMessage:
                wait = WebDriverWait(driver, 180).until(
                    ec.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
                driver.find_element_by_xpath('//span[@data-icon="send"]').click()
                break
            input_box.send_keys(Keys.CONTROL, "a")
            input_box.send_keys(Keys.DELETE)


def sendAttachment(file_path):
    wait = WebDriverWait(driver, 180).until(ec.element_to_be_clickable((By.XPATH, '//div[@title = "Attach"]')))
    attachement_section = driver.find_element_by_xpath('//div[@title = "Attach"]')
    attachement_section.click()
    image_box = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    image_box.send_keys(file_path)
    # wait upto images loads in page
    waitTillImageLoads()
    wait = WebDriverWait(driver, 180).until(ec.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]')))
    send_button = driver.find_element_by_xpath('//span[@data-icon="send"]')
    # time.sleep(1)
    wait = WebDriverWait(driver, 180).until(ec.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
    send_button.click()
    wait = WebDriverWait(driver, 180).until(
        ec.presence_of_element_located((By.XPATH, '//span[@data-icon="msg-check"]')))
    waitTillFileUploads()


def openClientChat(whatsapp_web_url):
    # Open a new window
    driver.execute_script("window.open('');")
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    driver.get(whatsapp_web_url)
    wait = WebDriverWait(driver, 180).until(ec.presence_of_element_located((By.ID, 'action-button')))
    continue_chat = driver.find_element_by_id('action-button')
    continue_chat.click()
    wait = WebDriverWait(driver, 180).until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'use WhatsApp Web')))
    skip_download = driver.find_element_by_partial_link_text("use WhatsApp Web")
    skip_download.click()


def closeClientChat():
    # close window after sending message and switch back to home window
    driver.execute_script("window.close('');")
    driver.switch_to.window(driver.window_handles[0])


def waitTillImageLoads():
    urlValid = False
    timeout_start = time.time()
    while True:
        # Load All Images on every itteration
        # time.sleep(1)
        images = driver.find_elements_by_tag_name('img')
        if time.time() < timeout_start + 120:
            for image in images:
                if ('blob' in image.get_attribute('src')):
                    urlValid = validateUrl(image.get_attribute('src').replace('blob:', ''))
                    if urlValid:
                        print('Image Uploaded Successfully!')
        else:
            print('Sending Image URL validation timed out !!!')
            raise
        if urlValid:
            break


def waitTillFileUploads():
    while True:
        media_upload = driver.find_elements_by_xpath('//span[@data-icon="media-upload"]')
        if not media_upload:
            print("File upload finished !")
            break

def validateUrl(blobUrl):
    return validators.url(blobUrl)