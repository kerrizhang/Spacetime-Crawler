import re
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.request
from urllib.parse import urlsplit
from urllib.parse import urlparse
import json
from utils import response
import pickle
# from collections import deque

linkqueue = []
uniquelinks = set()


def scraper(url, resp):
    if url[len(url) - 1:] == "/":
        url = url[:len(url) - 1]

    # if "?" in str(url):
    #     index = url.find("?")
    #     url = url[:index]

    linkqueue.append(url)
    uniquelinks.add(url)
    # links = extract_next_links(url, resp)
    #
    # for item in links:
    #     if is_valid(item):
    #         if item not in uniquelinks:
    #             linkqueue.append(item)
    #             uniquelinks.add(item)

    #print(linkqueue)
    while len(linkqueue) > 0:
        nextlink = linkqueue.pop(0)
        newlinks = extract_next_links(nextlink, get_response(nextlink))

        repeats = 0

        for item in newlinks:
            if is_valid(item) and resp.status == 200:
                if item not in uniquelinks:
                    linkqueue.append(item)
                    uniquelinks.add(item)
                    print(item) #UNCOMMENT TO PRINT OUT NEW LINKS
                else:
                    repeats = repeats + 1
            elif is_valid(item):
                print("Error: Status code was ", resp.status)

        print("Number of repeated urls: " + str(repeats))
        print("New number in queue: " + str(len(linkqueue)))
        print("Number of unique so far: " + str(len(uniquelinks)))
        print("_______________________________________________________________________________________________________________________")

    #return [link for link in links if is_valid(link)]


def extract_next_links(url, input_response):
    print("NOW EXTRACTING " + url)
    # Implementation requred.
    extracted_links = []
    
    # resp = requests.get(url)
    # txt = resp.text



    txt = input_response.raw_response

    soup = BeautifulSoup(txt, "html.parser")

    for link in soup.findAll('a'):
        link_href = link.get('href')
        #if is_valid(str(link_href)):
        if link_href == None:
            pass
        else:
            # if "?" in str(link_href):
            #     index = link_href.find("?")
            #     link_href = link_href[:index]

            if link_href[len(link_href) - 1:] == "/":
                link_href = link_href[:len(link_href) - 1]


            if link_href[0:1] == "/":
                if link_href[1:2] == "/":
                    extracted_links.append("http:" + link_href)
                else:
                    if(url[len(url) - 1:] == "/"):
                        extracted_links.append(url + link_href[1:])
                    else:
                        extracted_links.append(url + link_href)
            elif link_href[0:1] == "#":
                pass
            else:
                extracted_links.append(link_href)
    for link in extracted_links:
        if "#" in link:
            link = link[:link.find("#")]
        if "?" in link:
            #print("QUESTION MARK ?????????????????")
            link = link[:link.find("?")]


    return extracted_links






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
        resp_dict = {'url':url, 'status':resp.status_code, 'response': pickle.dumps(resp.text.encode())}

        return response.Response(resp_dict)
    except:
        print("Could not get response for URL")



def simhash(url):
    resp = get_response(url)
    txt = resp.raw_response
    #print(html2text.html2text(txt))
    soup = BeautifulSoup(txt, "html.parser")
    text = soup.get_text()

    l = tokenize(text)
    d = computeWordFrequencies(l)

    #vector = []
    vector = {}
    for i in d.keys():
        l = []
        hashnum = format(hash(i)%1024, '012b')
        for j in hashnum[2:]:
            l.append(j)
        vector[i] = l
        #print(vector)
      
    final = []
    for i in range(10):
        add = 0
        for k,v in vector.items():
            print(v[i])
            if v[i] == 1:
                add += d[k]
            elif v[i] == 0:
                add -= d[k]
            #print(add)
        final.append(add)
        print("========================")
    print(final)



    

    #print(text)

def tokenize(text):
    l = []
    for i in re.findall(r'[a-zA-Z0-9]{2,}', text):
        i = i.lower()
        l.append(i)
    return l

def computeWordFrequencies(tokens):
    d = {}
    for i in tokens:
        if i in d.keys():
            d[i]+=1
        else:
            d[i] = 1
    return d
    

        

    print(urlparse('http://www.ics.uci.edu/ugrad/courses/listing.php?year=2016&level=Graduate&department=STATS&program=ALL/about/about_factsfigures.php/community/alumni').netloc == urlparse('http://www.ics.uci.edu/ugrad/courses/listing.php?year=2016&level=Graduate&department=STATS&program=ALL/about/about_factsfigures.php/involved/leadership_council').netloc)


if __name__ == '__main__':

    #url = "https://www.ics.uci.edu/"
    url = "http://www.ics.uci.edu/ugrad/courses/listing.php?year=2016&level=Graduate&department=STATS&program=ALL/about/about_factsfigures.php/community/alumni"
    url2 = "http://www.ics.uci.edu/ugrad/courses/listing.php?year=2016&level=Graduate&department=STATS&program=ALL/about/about_factsfigures.php/involved"

    #resp = requests.get(url)
    #resp_dict = {'url':url, 'status':resp.status_code, 'response': pickle.dumps(resp.text.encode())} 

    #responseObj = response.Response(resp_dict)

    responseObj = get_response(url)

    print(simhash(url))
    
    #print(responseObj.raw_response)
    #print("#################################")
    #print(responseObj2.raw_response)

    

    #print(responseObj.raw_response)
    #print(responseObj.status)

    

    
    

    #scraper(url, responseObj)
    #print("Unique links: " + str(len(uniquelinks)))

    #print(resp)
    #print(resp.url)
    #print(test.json()['result'])
    
