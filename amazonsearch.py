from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import os

def search(search):
  AMAZON = "https://www.amazon.es/s?k={}"
  driver = webdriver.Remote(os.environ.get('BROWSER'), DesiredCapabilities.FIREFOX)

  search_term = '+'.join(search.split(' '))

  driver.get(AMAZON.format(search_term))

  results = []
  for idx in range(1,11):
    try:
      item = driver.find_element_by_xpath("//div[@data-index='{}']".format(idx))

      img = item.find_element_by_xpath(".//img")
      src = img.get_attribute('src')

      title_a = item.find_element_by_xpath(".//h2/a[@href]")
      title = title_a.text
      url = title_a.get_attribute('href')

      price_span = item.find_element_by_xpath(".//span[@class='a-price']")
      price = price_span.text

      result = {}
      result['src'] = src
      result['title'] = title
      result['url'] = url
      result['price'] = price
      result['source'] = 'amazon'

      results.append(result)

    except Exception as e:
      pass

  driver.close()

  return results