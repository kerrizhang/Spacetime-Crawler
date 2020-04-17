import re
from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
from urllib.parse import urlparse
from utils import response

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    new_urls = deque([url])
    processed_urls = set()
    domain_set_in = set()
    domain_set_out = set()
    broken_urls = set()
    # process urls one by one until we exhaust the queue
    while len(new_urls):  
        # move url from the queue to processed url set   
        url = new_urls.popleft()   
        processed_urls.add(url)
        # print the current url 
        print("Processings: " + url)
        try:    
            response = requests.get(url)
        except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):   
            broken_urls.insert(url)
            # add broken urls to it’s own set, then continue broken_urls.add(url)    continue
            # extract base url to resolve relative 
        
        
        
        parts = urlsplit(url) 

        print("Parts: ", parts)

        base = "{0.netloc}".format(parts)
        strip_base = base.replace("www.", "")
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if '/' in parts.path:
            path = url[:url.rfind('/')+1] 
        else:
            #url
            pass


        soup = BeautifulSoup(response.text, "lxml")
        for link in soup.find_all('a'):    
            # extract link url from the anchor    
            if "href" in link.attrs:
                anchor = link.attrs["href"]
            else:
                pass
        if anchor.startswith('/'):        
            local_link = base_url + anchor        
            local_urls.add(local_link)    
        elif strip_base in anchor:        
            local_urls.add(anchor)    
        elif not anchor.startswith('http'):        
            local_link = path + anchor        
            local_urls.add(local_link)    
        else:        
            foreign_urls.add(anchor)
        for i in local_urls:    
            if not i in new_urls and not i in processed_urls:        
                new_urls.append(i)
            if not link in new_urls and not link in processed_urls:    
                new_urls.append(link)

    return new_urls()



def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


if __name__ == '__main__':
    #a = response()
    extract_next_links("https://www.ics.uci.edu", 4)
    
