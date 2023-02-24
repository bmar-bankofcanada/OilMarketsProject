import mechanize
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup as bs
from numpy import equal
import json
import os

class OilMarketsScrapper():

    def __init__(self,email,password) -> None:
        '''
        Initiates the cookied and logs into the account
        '''
        cookie = CookieJar()
        self.req = mechanize.Browser()
        self.req.set_cookiejar(cookie)
        login_url = "https://account.jwnenergy.com/login?pub=DOB_BROWSE&continue=https%3A%2F%2Fwww.dailyoilbulletin.com%2Faccount%2Flogin%2F%3Fcontinue%3Dhttps%253A%252F%252Fwww.dailyoilbulletin.com%252F"
        self.req.open(login_url)
        self.req.select_form(nr=0)
        self.req.form['email'] = email
        self.req.form['password'] = password
        self.req.submit()

    def batch_scrapper(self,page_link,json_name,next_page=False,articles = []):
        '''
        Grabs all links within the page then loops and gets all the articles and there
        metadata and saves them to the json file. If next_page is True it will do this for
        each page until it grabs all the articles.
        '''
        self.req.open(page_link)
        headline_list = bs(self.req.response(),features="lxml").find('div',{"class":"category-list"})
        button = bs(self.req.response(),features='lxml').find('a',text='Next »')
        #This will loop through all articles and save them after each page is scrapped
        for a in headline_list.find_all("a"):
            try:
                self.req.open(a.get("href"))
                title_element = bs(self.req.response(),features='lxml').find('h1',{'class':'article-title'})
                if title_element is not None:
                    title = title_element.text
                else:
                    title = ""
                main_body = bs(self.req.response(),features="lxml").find('div',{'id':'article-body'})
                if main_body is not None:
                    text_element = main_body.find("div",{'id':'the-body-text'})
                    if text_element is not None:
                        text = text_element.text
                    sections_elements = main_body.find("a",{'itemprop':'articleSection'})
                    if sections_elements is not None:
                        sections = sections_elements.text
                    else:
                        sections = ""
                    categories_elements = main_body.find("ul",{'class':'article-categories'}).find_all("a")
                    if categories_elements is not None:
                        categories = []
                        for category in categories_elements:
                            categories.append(category.text)
                    else:
                        categories = ""
                else:
                    text = ""
                    sections = ""
                    categories = ""
                time_text = bs(self.req.response(),features='lxml').find('time',{'itemprop':'datePublished'})
                if time_text is not None:
                    time = time_text.text
                else:
                    time = ""
                
                article = {"title":title,"text":text,"section":sections,"categories":categories,"date":time}
                # article = {"text":text,"label":[]}
                articles.append(article)                
            except:
                pass
        
        with open(f'data/{json_name}.json','w') as fp:
            print("writing to json")
            json.dump({'data':articles},fp,indent=2)
            
            
        if next_page:
            if button is not None:
                next_link =button.get('href')
                self.batch_scrapper(next_link,json_name=json_name,next_page=next_page,articles=articles)