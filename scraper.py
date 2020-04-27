import re
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.request
from urllib.parse import urlsplit
from urllib.parse import urlparse
from urllib.parse import urljoin
import json
from utils import response
import pickle

# from collections import deque

linkqueue = []
uniquelinks = []
failedlinks = []
uniqueurls = set()
stopwords = []
commonwordsdict = dict()
subdomains = dict()
longestlength = 0



def scraper(url, resp):
    links = extract_next_links(url, resp)
    #print("Links: ", links)
    return [link for link in links if is_valid(link)]
    '''
    global longestlength
    f = open("stopwords.txt")
    for line in f:
        stopwords.append(line.strip("\n"))
    f.close()

    begincheck = url
    if url[-1] == "/":
        begincheck = url[:-1]

    linkqueue.append(url)
    uniquelinks.append(simhash(url))
    uniqueurls.add(begincheck)

    while len(linkqueue) > 0:
        nextlink = linkqueue.pop(0)
        newlinks = extract_next_links(nextlink, get_response(nextlink))

        repeats = 0
        newadded = 0

        for item in newlinks:
            tempcheck = item
            if item[-1] == "/":
                tempcheck = item[:-1]
            if tempcheck not in uniqueurls:
                if is_valid(item) and resp.status == 200:

                    ####### SUBDOMAIN 
                    subd = urlparse(item).netloc
                    if subd in subdomains:
                        subdomains[subd] += 1
                        print("Subdomain ", subd, ": ", subdomains[subd] )
                    else:
                        subdomains[subd] = 1
                        print("New subdomain " + subd)

                    temp = simhash(item)
                    item_simhash = temp[0]
                    worddict = temp[1]
                    curlen = 0
                    for t in worddict.items():
                        curlen += t[1]
                    if curlen > longestlength:
                        longestlength = curlen
                    if item_simhash[0] != 2:
                        if item_simhash not in uniquelinks:
                            for word in worddict:
                                if word in commonwordsdict:
                                    commonwordsdict[word] += worddict[word]
                                else:
                                    commonwordsdict[word] = worddict[word]
                            linkqueue.append(item)
                            uniquelinks.append(item_simhash)
                            uniqueurls.add(tempcheck)
                            newadded = newadded + 1
                            print("new link! " + item)  # UNCOMMENT TO PRINT OUT NEW LINKS
                            #print(commonwordsdict)
                            # print(simhash(item))
                        else:
                            repeats = repeats + 1
                            print("this is content repeat: " + item)  # UNCOMMENT TO SEE CONTENT REPEATS
                            uniqueurls.add(tempcheck)
                            # print(simhash(item))
                    else:
                        print("Simhash had a 2")
                elif is_valid(item):
                    print("Error: Status code was ", resp.status)
            else:
                repeats = repeats + 1
                print("this is a url  repeat: " + item)  # UNCOMMENT TO SEE URL REPEATS

        print("Number of repeated urls: " + str(repeats))
        print("New number in queue: " + str(len(linkqueue)))
        print("Number of newly added links: " + str(newadded))
        print("Number of unique so far: " + str(len(uniquelinks)))

        print("Number of subdomains so far: " + str(len(subdomains.keys())))
        print(
            "_____________________________________________________________________________________________________________________")
    '''


def extract_next_links(url, input_response):
    print("NOW EXTRACTING " + url)
    #print(longestlength)
    # Implementation requred.
    extracted_links = []

    if input_response == None:
        return []

    print("1")
    try:
        txt = input_response.raw_response.content
    except:
        print("No content in raw response")
        return []
    

    try:
        soup = BeautifulSoup(txt, "html.parser")

        for link in soup.findAll('a'):
            link_href = link.get('href')
            if link_href == None:
                pass
            else:
                # if link_href[len(link_href) - 1:] == "/":
                #     link_href = link_href[:len(link_href) - 1]
                # print(link_href)
                # print(urlparse(url).path)

                extracted_links.append(urljoin(url, link_href))

        for i, e in enumerate(extracted_links):
            if "#" in e:
                extracted_links[i] = extracted_links[i][:e.find('#')]


        # for i, e in enumerate(extracted_links):
        #     if e[len(e) - 1:] == "/":
        #         extracted_links[i] = e[:len(e) - 1]

        return extracted_links

    except:
        print("Beautiful soup failed")
        return []
        


def is_valid(url):
    try:
        if "/pdf/" in url or "mailto:" in url or "@" in url:
            return False
        parsed = urlparse(url)
        # print(parsed.netloc)
        if parsed.netloc == "" and str(parsed.path)[0:len(
                "today.uci.edu/department/information_computer_sciences")] == "today.uci.edu/department/information_computer_sciences":
            return True

        if parsed.scheme not in set(["http", "https"]):
            return False


        if ("ics.uci.edu" in parsed.netloc or "cs.uci.edu" in parsed.netloc or "informatics.uci.edu" in parsed.netloc or "stat.uci.edu" in parsed.netloc):
            if (re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", url.lower())):
                    return False
            return not re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|war|"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
        return False

    except TypeError:
        print("TypeError for ", parsed)
        # raise



def get_response(url):
    try:
        resp = requests.get(url)
        resp_dict = {'url': url, 'status': resp.status_code, 'response': pickle.dumps(resp.text.encode())}

        return response.Response(resp_dict)
    except:
        print("Could not get response for URL")


def similarity(l1, l2):
    num = 0
    for i in range(10):
        if l1[i] == l2[i]:
            num += 1
    return num / 10


def simhash(url):
    resp = get_response(url)
    if (resp == None):
        print("This url has an empty response: " + url)
        failedlinks.append(url)
        return ([2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dict())
    txt = resp.raw_response
    
    try:
        soup = BeautifulSoup(txt, "html.parser")
        text = soup.get_text()
        d = computeWordFrequencies(tokenize(text))
        vector = {}
        for i in d.keys():
            l = []
            hashnum = format(hash(i) % 32768, '015b')
            for j in hashnum:
                l.append(j)
            vector[i] = l
        final = []
        for i in range(13):
            add = 0
            for k, v in vector.items():
                if v[i] == '1':
                    add += d[k]
                else:
                    add -= d[k]
            final.append(add)

        ans = []
        for i in final:
            if i > 0:
                ans.append(1)
            else:
                ans.append(0)
        return (ans, d)

    except:
        print("Beautiful soup failed")
        return ([2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dict())


def tokenize(text):
    l = []
    for i in re.findall(r'[a-zA-Z0-9]{2,}', text):
        i = i.lower()
        l.append(i)
    return l


def computeWordFrequencies(tokens):
    freq_dict = {}
    for i in tokens:
        if i not in stopwords:
            if i in freq_dict.keys():
                freq_dict[i] += 1
            else:
                freq_dict[i] = 1
    return freq_dict


if __name__ == '__main__':
    url = "http://www.vision.ics.uci.edu"
    url2 = "https://www.cs.uci.edu"
    url3 = "https://www.informatics.uci.edu"
    url4 = "https://www.stat.uci.edu"

    #urltest = "http://www.vision.ics.uci.edu"
    urltest = "http://www.ics.uci.edu/about"


    responseObj = get_response(url)
    responseObj2 = get_response(url2)
    responseObj3 = get_response(url3)
    responseObj4 = get_response(url4)

    scraper(url, responseObj)
    scraper(url2, responseObj2)
    scraper(url3, responseObj3)
    scraper(url4, responseObj4)
    
    print("TOTAL Unique links: " + str(len(uniquelinks)))
    print("FAILED LINKSSS: " + str(failedlinks))

    # responseObj = get_response(urltest)
    # scraper(urltest, responseObj)
