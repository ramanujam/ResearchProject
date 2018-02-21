# -*- coding: utf-8 -*-
from   bs4            import BeautifulSoup
import csv
import datetime
import json
import logging
import os
import random
import re
import requests
import urllib
import xlsxwriter
from optparse import OptionParser
from   web2screenshot import make_screenshot


# create logger
logger = logging.getLogger('GoogleSearchLogger')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
fh = logging.FileHandler('../logs/google_search_{:%Y%m%d}.log'.format(datetime.datetime.now()))
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(fh)
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')

cols = [
        "City",
        "State",
        "Datetime",
        "Search term",
        "Google URL",
        "Ad URL Website",
        "Website Name",
        "Vendor",
        "Position Num",
        "Position",
        "Result is consistent",
        "Page number",
        "Type of result",
        "Comments",
        "Ad Value",
        "Static File Path"]

# the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,
# netscape for more user agent strings,you can find it in
# http://www.useragentstring.com/pages/useragentstring.php

user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]
# Organic result class


class organic:
    def __init__(self, name):
        self.product_name = name
        self.type = "organic"

    def to_string(self):
        msg  = self.type + " Product Name   : %s\n"   % self.product_name
        msg += self.type + " Product URL    : %s\n"   % self.product_url
        msg += self.type + " Product Price  : %s\n"   % self.price
        msg += self.type + " Product Vendor : %s\n"   % self.vendor
        msg += self.type + " file location  : %s\n\n" % self.filename
        return msg


    def get_random_filename(self):
        vendor  = re.sub('[^0-9a-zA-Z]+', '_', self.vendor)
        product = re.sub('[^0-9a-zA-Z]+', '_', self.product_name)
        self.filename = "../data/" + self.type + product[:15] + vendor + str(random.randint(1, 100000)) + ".png"
        self.filename = os.path.abspath(self.filename)

    def convert_url_to_pdf(self):
        self.get_random_filename()
        try:
            if "http" not in self.product_url:
                www = re.compile("(w{3,})")
                if(www.match(self.product_url)):
                    self.product_url = "http://" + self.product_url
                else:
                    logger.debug("Can't find http in URL : please check.\nURL %s\n", self.product_url)
                    self.filename = "NA"
                    return
            make_screenshot(self.product_url, self.filename)
        except Exception as e:
            logger.exception("message")
            self.filename = "NA"


# Advertisement class
class advertiz(organic):
    def __init__(self, name):
        self.product_name = name
        self.type         = "SponsoredAd"

class SearchResult:
    def __init__(self, keyword):
        self.keyword = keyword
        self.address = "http://www.google.com/search?q=%s&num=20&hl=en&start=0" % (urllib.parse.quote_plus(keyword))
        self.user    = self.process_request()
        self.request = urllib.request.Request(self.address, None, {'User-Agent': self.user})
        self.ads     = []
        # call search
        self.get_google_search_result()
        self.parse_ads()
        self.convert_to_csv()

    def process_request(self):
        ua = random.choice(user_agent_list)
        return ua

    def get_google_search_result(self):
        self.urlfile = urllib.request.urlopen(self.request)
        self.page    = self.urlfile.read().decode('utf-8')
        self.soup    = BeautifulSoup(self.page, 'html.parser')
        self.get_location()

    def get_location(self):
        try:
          url          = 'http://freegeoip.net/json'
          r            = requests.get(url)
          j            = json.loads(r.text)
          logger.info("Trying to get location : {} ".format(j))
          self.city    = j['city']
          self.state   = j['region_code']
        except Exception as e:
          logger.info("Can't reach FREEGEOIP")
          logger.info(e)
	  
	
    def to_string(self):
        print("Keyword : %s" % self.keyword)
        print("Address : %s" % self.address)
        print("Title   : %s" % self.soup.title.string)
        print("City    : %s" % self.city)
        print("State   : %s" % self.state)

    def parse_ads(self):
        # get top ads
        self.parse_top_ads()
        # get right ads
        self.parse_right_ads()
        #get bottom ads
        self.parse_bottom_ads()
        #get_organic_results
        self.parse_organic_results()

    # todo - all the ads

    def parse_right_ads(self):
        try:
            self.right_ads = self.soup.find(id="rhs_block")
            ad_data = self.right_ads.find('span' , {"class" : "_Ei rhsg4"})
            self.right_ad_list = self.right_ads.find_all('div' , {"class": "_Dw"})
            for item in self.right_ad_list:
                # create ad object
                ad                = advertiz(ad_data.get_text())
                ad.location       = "RHS"
                ad.product_url    = item.find('a', {"class":"plantl"})['href']
                ad.price          = item.find('span', {"class": "_kh"}).text
                ad.vendor         = item.find('span' , {"class" :"rhsl4"}).text
                ad.convert_url_to_pdf()
                self.ads.append(ad)
        except Exception as e:
            logger.info("Unable to parse right_ads\n", e)
            logger.debug("Right side not parsed.... ", e)

    def parse_top_ads(self):
        try:
            self.top_ads = self.soup.find("div", {"id": "taw"})
            self.top_ads_list = self.top_ads.find_all(class_="mnr-c pla-unit")
        except Exception as e:
            logger.info("Unable to parse top_ads\n", e)
            logger.debug("top ads not parsed.... ", e)

        for item in self.top_ads_list:
            try:
                ad_data        = item.find('a', {"class" : "plantl pla-unit-title-link"})

                # create ad object
                ad             = advertiz(ad_data.span.text)
                ad.location    = "top"
                ad.product_url = ad_data['href']
                ad.price       = item.find(class_="_QD _pvi").get_text()
                ad.vendor      = item.find(class_="_mC").get_text()
                ad.convert_url_to_pdf()
                self.ads.append(ad)
            except Exception as e:
                logger.debug(ad_data.prettify())


    def parse_bottom_ads(self):
        try:
            self.bottom_ads      = self.soup.find("div", {"id": "bottomads"})
            self.bottom_ads_list = self.bottom_ads.find_all('li' , {"class":"ads-ad"})
            for item in self.bottom_ads_list:
                ad_data        = item.find('a', {"class" : re.compile("(_.+) ")})
                # create ad object
                ad             = advertiz(ad_data.text)
                ad.location    = "bottom"
                ad.product_url = item.find('div', {"class" : "ads-visurl"}).find('cite').text
                ad.price       = "NA"
                ad.vendor      = self.get_vendor_from_organic(ad.product_url)
                ad.convert_url_to_pdf()
                self.ads.append(ad)
        except Exception as e:
            logger.info("Unable to parse bottom_ads\n", e)
            logger.debug("bottom ads not parsed.... " , e)

    def parse_organic_results(self):
        try:
            self.organic            = self.soup.find('div', {"class":"srg"})
            self.organic_list       = self.organic.find_all('div', {"class":"g"})
            count = 1;
            for item in self.organic_list:
                item_data           = item.find('h3', {"class":"r"}).find('a')
                item_name           = item_data.text
                oresult             = organic(item_name)
                oresult.product_url = item_data['href']
                logger.debug("Got url " + item_data['href'])
                oresult.vendor      = self.get_vendor_from_organic(item_data['href'])
                logger.debug("Got vendor " + oresult.vendor)
                oresult.location    = "organic :"  + str(count)
                count               = count + 1
                oresult.price       = self.get_price_from_organic(item)
                print("Got_price :", oresult.price)
                oresult.convert_url_to_pdf()
                oresult.to_string()
                self.ads.append(oresult)
        except Exception as e:
            logger.debug("Error while parsing organic result\n", e)

    def convert_to_csv(self):
      try:
        row = 0
        col = 0
        workbook = xlsxwriter.Workbook('~/ResearchProject/GoogleSearch/data/SearchResult.xlsx')
        worksheet = workbook.add_worksheet("ProductDetails")
        for j, t in enumerate(cols):
          worksheet.write(row, col + j, t)
        for ad  in self.ads: 
          row = row + 1
          row_elements = self.get_spreadsheet_row(ad)
          for i in range(len(cols)):
            if (cols[i] == "Static File Path" or cols[i] == "Google URL" or cols[i] == "Ad URL Website"):
              worksheet.write_url(row, i, row_elements[i])
            else:
              worksheet.write(row, i, row_elements[i])
        workbook.close()

      except Exception as e:
        logger.debug("Unable to open file 'Ads.xlsx' to write data\n", e)

    def get_vendor_from_organic(self, text):
        vendor_ex = re.compile(r"http[s]?\W+w{0,3}[\.]?(.*?)\.")
        vendor = vendor_ex.search(text)
        logger.debug("Vendor text : " + text)
        if vendor is None:
            return text
        return vendor.group(1)

    def get_price_from_organic(self, item):
        price_ex = re.compile(r"(\$\d+[\.\d]+)\b")
        try:
            text_to_search = item.find('div', {"class":"slp f"}).text
            print(text_to_search)
            price    = price_ex.search(text_to_search)
        except:
            logger.debug("Unable to find price")
            price = None
        if price is None:
            return "NA"
        else:
            return price.group(1)
    def get_spreadsheet_row(self, ad):
      row = [self.city, self.state, datetime.datetime.now(), self.keyword, \
             self.address, ad.product_url, ad.vendor, "NA", "NA", ad.location, \
             "NA", "1", ad.type, "NA", ad.price, "file://"+ad.filename]
      return row

def main():
    parser = OptionParser()
    parser.add_option("-p", "--product_name", dest = "product_name", help="Enter the product you want to search")
    (options, args) = parser.parse_args()
    ad_result = SearchResult(options.product_name)
    logger.debug(ad_result.to_string())

if __name__ == "__main__":
    main()
