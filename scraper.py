import re
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.request
from urllib.parse import urlsplit
from urllib.parse import urlparse
import json
from utils import response
# from collections import deque

linkqueue = []
uniquelinks = set()


def scraper(url, resp):

    links = extract_next_links(url, resp)

    for item in links:
        if is_valid(item):
            if item not in uniquelinks:
                linkqueue.append(item)
                uniquelinks.add(item)

    #print(linkqueue)
    while len(linkqueue) > 0:
        nextlink = linkqueue.pop(0)
        newlinks = extract_next_links(nextlink, requests.get(nextlink))

        for item in newlinks:
            if is_valid(item):
                if item not in uniquelinks:
                    linkqueue.append(item)
                    uniquelinks.add(item)
                    print(item)

        print("New number in queue: " + str(len(linkqueue)))

    #return [link for link in links if is_valid(link)]


def extract_next_links(url, input_response):
    print("NOW EXTRACTING " + url + "       ________________________________________________________________________________________________________________")
    # Implementation requred.
    extracted_links = []
    
    # resp = requests.get(url)
    # txt = resp.text

    if input_response.status == 200:   # THIS NEEDS TO BE IMPROVED ############

        txt = input_response.raw_response

        soup = BeautifulSoup(txt, "html.parser")
        
        for link in soup.findAll('a'):
            link_href = link.get('href')
            #if is_valid(str(link_href)):
            if link_href == None:
                pass
            else:
                if link_href[0:1] == "/":
                    if link_href[1:2] == "/":
                        extracted_links.append("http:" + link_href)
                    else:
                        extracted_links.append(url + link_href)
                elif link_href[0:1] == "#":
                    pass
                else:
                    extracted_links.append(link_href)
        for link in extracted_links:
            if "#" in link:
                link = link[:link.find("#")]


        return extracted_links


    else:
        print("Error: Status code was ", input_response.status)





def is_valid(url):
    try:
        parsed = urlparse(url)
        if  parsed.netloc == "" and str(parsed.path)[0:len("today.uci.edu/department/information_computer_sciences")] == "today.uci.edu/department/information_computer_sciences":
            return True
        if parsed.scheme not in set(["http", "https"]):
            return False
        if parsed.netloc not in set(["ics.uci.edu", "www.ics.uci.edu", "cs.uci.edu", "www.cs.uci.edu", "informatics.uci.edu", "www.informatics.uci.edu", "stat.uci.edu", "www.stat.uci.edu"]): 
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


def get_response(url):
    try:
        resp = requests.get(url)
        resp_dict = {'url':url, 'status':resp.status_code, 'response': open(str.encode(resp.text))}

        return response.Response(resp_dict)
    except:
        print("Could not get response for URL")
        



if __name__ == '__main__':
    #a = response()
    #is_valid("https://ics.uci.edu/something")
    #is_valid("https://google.com/something")
    #is_valid("https://today.uci.edu/department/information_computer_sciences/one/?something#three")
    #is_valid("today.uci.edu/department/information_computer_sciences/something")
    
    #scraper("https://www.ics.uci.edu", requests.get("https://www.ics.uci.edu"))
    #resp = Response()
    #print("Unique links: " + str(len(uniquelinks)))



    url = "https://www.ics.uci.edu"

    resp = requests.get(url)
    resp_dict = {'url':url, 'status':resp.status_code, 'response': open(str.encode(resp.text))} # THIS IS NOT CORRECT KERRI ####### 

<<<<<<< Updated upstream
    resp_dict = {'url':url, 'status':resp.status_code, 'response': open(str.encode(resp.text))}
=======
>>>>>>> Stashed changes
    responseObj = response.Response(resp_dict)

    #responseObj = get_response(url)

    #print(responseObj.status)

    

    
    

    #scraper("https://www.ics.uci.edu", responseObj)

    #print(resp)
    #print(resp.url)
    #print(test.json()['result'])
    
