from bs4 import BeautifulSoup # For HTML parsing                                                                                                                         
import urllib2 # Website connections
import re # Regular expressions
import numpy as np
import sys

RESUME_URL_PATTERN = re.compile("^window.open\('/r/(.+)', '_blank'\)$")

def extract_resume_url(js):
    m = RESUME_URL_PATTERN.match(js)
    if m:
        return m.groups()[0]
    return None

def fetch_url(url):
    try:
        page = urllib2.urlopen(url).read() # Connect to the job posting
        soup_obj = BeautifulSoup(page) # Get the html from the site
        if len(soup_obj) == 0: # In case the default parser lxml doesn't work, try another one
            return BeautifulSoup(page, 'html5lib')
        return soup_obj
    except: 
        return None

def has_PhD(text):
    for i in ['Ph.D','PHD', 'PhD','Doctorate of Philosophy','Ph. D', 'Ph.D.']:
        if text.find(i):
           return True
    return False
    
def indeed_scraper():

    URL = 'http://www.indeed.com/resumes?q=data+scientist&l=WA&co=US&start=%s' % sys.argv[1]
    with open('company.txt', "ab") as MYfile:
        listings = fetch_url(URL)
        print(listings)
        if listings:
            lines=listings.find_all('li','sre') 

            for line in lines:
                comps = []
                exps = line.find_all('div',class_='experience')
                for exp in exps:
                    comp = exp.find('span',class_='company')
                    if comp:
                       #print('    ', comp.text, exp.text)
                       comps.append(comp.text)
                edus = line.find_all('div', class_='education')
                for edu in edus:
                    univ = edu.find('span',class_='degree')
                    if univ:
                       print('    ', univ.text)
                       if has_PhD(univ.text):
                          print(' ==> company names', comps)
                          MYfile.write('\t'.join(comps)) 
                          MYfile.write('\n') 
                          
        else:
            print("Failed to fetch listings.")
        return
   
if __name__ == '__main__':
    indeed_scraper()    
