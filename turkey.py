from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import os
from time import sleep

def get_data(start, end):
  driver = webdriver.Remote('http://192.168.1.35:4445/wd/hub', DesiredCapabilities.CHROME)
  url = 'https://www.tefas.gov.tr/FonKarsilastirma.aspx'
  driver.get(url)
  driver.find_element_by_xpath("//input[@id='MainContent_TextBoxStartDate']").clear()
  driver.find_element_by_xpath("//input[@id='MainContent_TextBoxStartDate']").send_keys(start)
  driver.find_element_by_xpath("//input[@id='MainContent_TextBoxEndDate']").clear()
  driver.find_element_by_xpath("//input[@id='MainContent_TextBoxEndDate']").send_keys(end)
  driver.find_element_by_xpath("//input[@id='MainContent_ButtonSearchDates']").click()
  driver.find_element_by_xpath("//input[@id='MainContent_ImageButtonExcelGenel']").click()

  sleep(3)
  driver.close()

if __name__ == "__main__":
  get_data('01.01.2020', '01.02.2020')