# IMPORTING MODULES ------------------------------------------------------------------------------------------------------------
import scrapy

# import Pandas as pd
# ------------------------------------------------------------------------------------------------------------------------------

# CREATING CLASS FOR SCRAPING---------------------------------------------------------------------------------------------------
class ShopSpider(scrapy.Spider):
    name = 'SHOPSPIDER'
    page_value=2
    #CONSTRUCTOR----------------------------------------------------------------------------------------------------------------
    def __init__(self,value,pages=50):
        self.start_urls = [f'https://www.shopclues.com/ajaxCall/searchProducts?q={value}&z=1&page=1&filters=&fl_cal=1&sc_z=1111'] 
        self.value=value
        self.pages=pages
        super().__init__(self.name) 
    #---------------------------------------------------------------------------------------------------------------------------
 
    #PARSE FUNCTION-------------------------------------------------------------------------------------------------------------
    def parse(self,response):
        sublinks=response.css('div.column a[target="_blank"]::attr(href)').extract()# EXTRACTING ALL THE PRODUCT LINKS
        for url in sublinks:                                                        # For each link in products link
            if 'https:' not in url:
                url='https:'+url
            yield scrapy.Request(url=url,callback=self.parse_page)                  # Calling Parse Page function

        if self.page_value<self.pages:
            next_url=f'https://www.shopclues.com/ajaxCall/searchProducts?q={self.value}&z=1&page={self.page_value}&filters=&fl_cal=1&sc_z=1111'
            self.page_value+=1
            yield scrapy.Request(next_url,self.parse)          
    #----------------------------------------------------------------------------------------------------------------------------------------------

    #PARSE PAGE FUNCTION---------------------------------------------------------------------------------------------------------------------------
    def parse_page(sel,response):

        try:
            title=response.css('h1[itemprop="name"]::text').extract_first()             # TITLE
            title=title.strip()           
        except:
            title=""
        try:
            cat=response.css('span[itemprop="title"]::text').extract()                  # CATEGORIES
            product=cat[-1]                                                             # PRODUCT TYPE                                               # SUB CATEGORY
        except Exception as e:
            print(e)
        
        price=response.css('span.f_price::attr(content)').extract_first()               # PRICE OF THE PRODUCT
        price=price+"Rs"
        try:
            rating=response.css('span[itemprop="ratingValue"]::text').extract_first()   # USER RATING 
        except:
            rating=""
        try:
            seller=response.css('h3[itemprop="name"]::text').extract_first()            # SELLER OF THE PRODUCT
        except:
            seller=""
        yield {                                                                         # STORING DATA
            "NAME":title,
            "PRODUCT":product,
            "PRICE":price,
            "RATING":rating,
            "SELLER":seller
        }
    #---------------------------------------------------------------------------------------------------------------------
# END OF THE CLASS--------------------------------------------------------------------------------------------------------

# COMMAND - scrapy runspider shop2.py -a value=sarees -o sarees.csv