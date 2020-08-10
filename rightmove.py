from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import os
from pprint import pprint
import re

def search(location):
  url = 'https://www.rightmove.co.uk/property-for-sale/search.html?searchLocation={}&locationIdentifier=&useLocationIdentifier=false&buy=For+sale'
  location = 'London'
  driver = webdriver.Remote(os.environ.get('BROWSER'), DesiredCapabilities.FIREFOX)
  driver.get(url.format(location))
  submit_btn = driver.find_element_by_xpath("//button[@id='submit']").click()
  links_a = driver.find_elements_by_xpath("//a[@class='propertyCard-link']")[0:10]
  links = [x.get_attribute('href') for x in links_a]

  properties = []
  for link in links:
    driver.get(link)

    try:
      address = driver.find_element_by_xpath("//address[@itemprop='address']").text
    except Exception as e:
      address = ''


    try:
      title = driver.find_element_by_xpath("//h1[@itemprop='name']").text

    except Exception as e:
      title = ''

    try:
      price = driver.find_element_by_xpath("//p[@id='propertyHeaderPrice']/strong").text

    except Exception as e:
      price = ''

    try:
      src = driver.find_element_by_xpath("//img[@class='js-gallery-main']").get_attribute('src')

    except Exception as e:
      src = ''

    # key features
    try:
      key_features_list = driver.find_elements_by_xpath("//div[@class='sect key-features']/ul/li")
      key_features = [x.text for x in key_features_list]
      bedrooms = next((x.replace('bedrooms', '') for x in key_features if 'bedrooms' in x), 0)
      bathrooms = next((x.replace('bathrooms', '') for x in key_features if 'bathrooms' in x), 0)

    except Exception as e:
      bedrooms = 0
      bathrooms = 0

    if bedrooms == 0 and 'bedroom' in title:
      try:
        bedrooms = title.split('bedroom')[0]

      except Exception as e:
        pass

    try:
      location_element = driver.find_element_by_xpath("//a[@href='#location']/img")
      location_url = location_element.get_attribute('src')

      latitude = re.search(r'latitude=(.*?)&', location_url).group(1)
      longitude = re.search(r'longitude=(.*?)&', location_url).group(1)

    except Exception as e:
      latitude = ''
      longitude = ''


    result = {}
    result['link'] = link
    result['address'] = address
    result['title'] = title
    result['price'] = price
    result['src'] = src
    result['bedrooms'] = bedrooms
    result['bathrooms'] = bathrooms
    result['latitude'] = latitude
    result['longitude'] = longitude

    properties.append(result)


  return properties

if __name__ == "__main__":
  pprint(search('London'))