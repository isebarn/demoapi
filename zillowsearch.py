import os
from pprint import pprint
import urllib3
from bs4 import BeautifulSoup, SoupStrainer
from multiprocessing import Pool


def get_page_by_urllib3(url):
  http = urllib3.PoolManager()
  response = http.request("GET", url)

  return response

def parse(url):
  response = get_page_by_urllib3(url)
  soup = BeautifulSoup(response.data, features="lxml")

  price = soup.find("span", class_= 'ds-value').text
  zestimate = soup.find("div", id='ds-home-values').find('span').next_sibling.text
  info = soup.find_all("span", class_='ds-bed-bath-living-area')
  info_text = [x.text for x in info]
  bedrooms = next((x for x in info_text if 'bd' in x), '0').split(' bd')[0]
  bathrooms = next((x for x in info_text if 'ba' in x), '0').split(' ba')[0]
  area = next((x for x in info_text if 'sqft' in x), '0').split(' sqft')[0]
  src = soup.find("source", {'type': 'image/webp'})['srcset'].split(',')[0].split(' ')[0]



  result = {}
  result['price'] = price
  result['zestimate'] = zestimate
  result['bedrooms'] = bedrooms
  result['bathrooms'] = bathrooms
  result['area'] = area
  result['url'] = url
  result['src'] = src


  return result


def zip_search(search_term):
  response = get_page_by_urllib3('https://www.zillow.com/homes/{}_rb/')
  soup = BeautifulSoup(response.data, features="lxml")
  url_divs = soup.find_all('div', class_='list-card-top')[0:5]
  urls = [div.findChild('a')['href'] for div in url_divs]

  pool = Pool(processes=2)
  result = pool.map(parse, urls)
  
  return result


if __name__ == "__main__":
  r = parse('https://www.zillow.com/homedetails/998-Butler-Dr-Crystal-Lake-IL-60014/5055871_zpid/')
  #print(r)