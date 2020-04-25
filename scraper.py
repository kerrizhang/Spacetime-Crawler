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
uniquelinks = []
failedlinks = []
uniqueurls = []
stopwords = []


def scraper(url, resp):
    f = open("stopwords.txt")
    for line in f:
        stopwords.append(line.strip("\n"))
    f.close()

    if url[len(url) - 1:] == "/":
        url = url[:len(url) - 1]
    # if "?" in str(url):
    #     index = url.find("?")
    #     url = url[:index]

    linkqueue.append(url)
    uniquelinks.append(simhash(url))
    uniqueurls.append(url)
    # links = extract_next_links(url, resp)
    #
    # for item in links:
    #     if is_valid(item):
    #         if item not in uniquelinks:
    #             linkqueue.append(item)
    #             uniquelinks.add(item)

    # print(linkqueue)
    while len(linkqueue) > 0:
        nextlink = linkqueue.pop(0)
        newlinks = extract_next_links(nextlink, get_response(nextlink))

        repeats = 0
        newadded = 0

        for item in newlinks:
            if item not in uniqueurls:
                # print("----------" + item)
                if is_valid(item) and resp.status == 200:

                    item_simhash = simhash(item)
                    if item_simhash[0] != 2:
                        if item_simhash not in uniquelinks:
                            linkqueue.append(item)
                            uniquelinks.append(item_simhash)
                            uniqueurls.append(item)
                            newadded = newadded + 1
                            print("new link! " + item)  # UNCOMMENT TO PRINT OUT NEW LINKS
                            # print(simhash(item))
                        else:
                            repeats = repeats + 1
                            print("this is content repeat: " + item)  # UNCOMMENT TO SEE CONTENT REPEATS
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
        print(
            "_____________________________________________________________________________________________________________________")
    # return [link for link in links if is_valid(link)]


def extract_next_links(url, input_response):
    print("NOW EXTRACTING " + url)
    # Implementation requred.
    extracted_links = []

    # resp = requests.get(url)
    # txt = resp.text

    if input_response == None:
        return []

    txt = input_response.raw_response

    soup = BeautifulSoup(txt, "html.parser")

    for link in soup.findAll('a'):
        link_href = link.get('href')
        # if is_valid(str(link_href)):
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
                    if (url[len(url) - 1:] == "/"):
                        extracted_links.append(urlparse(url).netloc + link_href[1:])
                    else:
                        extracted_links.append(urlparse(url).netloc + link_href)
            elif link_href[0:1] == "#":
                pass
            elif link_href[0:2] == "..":
                extracted_links.append(urlparse(url).netloc + link_href[2:])
            elif link_href[0:4] == "http":
                extracted_links.append(link_href)
            else:
                extracted_links.append(url + "/" + link_href)

    for i, e in enumerate(extracted_links):
        if "#" in e:
            extracted_links[i] = extracted_links[i][:e.find('#')]

        # if "?" in link:
        #     #print("QUESTION MARK ?????????????????")
        #     link = link[:link.find("?")]

    for i, e in enumerate(extracted_links):
        if e[len(e) - 1:] == "/":
            extracted_links[i] = e[:len(e) - 1]

    return extracted_links


def is_valid(url):
    try:
        if "/pdf/" in url or "mailto:" in url or "@" in url:
            return False
        parsed = urlparse(url)
        if parsed.netloc == "" and str(parsed.path)[0:len(
                "today.uci.edu/department/information_computer_sciences")] == "today.uci.edu/department/information_computer_sciences":
            return True
        if parsed.scheme not in set(["http", "https"]):
            return False
        if (
                "ics.uci.edu" in parsed.netloc or "cs.uci.edu" in parsed.netloc or "informatics.uci.edu" in parsed.netloc or "stat.uci.edu" in parsed.netloc):
            return not re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
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
    # print(url_dict)
    resp = get_response(url)
    if (resp == None):
        print("This url has an empty response: " + url)
        failedlinks.append(url)
        return [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    txt = resp.raw_response
    # print(html2text.html2text(txt))
    soup = BeautifulSoup(txt, "html.parser")
    text = soup.get_text()

    d = computeWordFrequencies(tokenize(text))
    # vector = []
    vector = {}
    for i in d.keys():
        l = []
        hashnum = format(hash(i) % 8192, '013b')
        for j in hashnum:
            l.append(j)
        vector[i] = l
        # print(vector)
    final = []
    for i in range(13):
        add = 0
        for k, v in vector.items():
            if v[i] == '1':
                add += d[k]
            else:
                add -= d[k]
            # print(add)
        final.append(add)
    # return final
    # print(final)

    ans = []
    for i in final:
        if i > 0:
            ans.append(1)
        else:
            ans.append(0)
    return ans

    # print(text)


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

    # print(urlparse('http://www.ics.uci.edu/ugrad/courses/listing.php?year=2016&level=Graduate&department=STATS&program=ALL/about/about_factsfigures.php/community/alumni').netloc == urlparse('http://www.ics.uci.edu/ugrad/courses/listing.php?year=2016&level=Graduate&department=STATS&program=ALL/about/about_factsfigures.php/involved/leadership_council').netloc)


if __name__ == '__main__':
    url = "https://www.ics.uci.edu"

    # url = "http://www.ics.uci.edu/ugrad/courses/listing.php?year=2016&level=Graduate&department=STATS&program=ALL/about/about_factsfigures.php/community/alumni"
    # url2 = "http://www.ics.uci.edu/ugrad/courses/listing.php?year=2016&level=Graduate&department=STATS&program=ALL/about/about_factsfigures.php/involved"

    # resp = requests.get(url)
    # resp_dict = {'url':url, 'status':resp.status_code, 'response': pickle.dumps(resp.text.encode())}

    # responseObj = response.Response(resp_dict)

    responseObj = get_response(url)

    # print(simhash(url2))
    # print(simhash(url))
    # print(similarity(simhash(url2), simhash(url)))

    # print(responseObj.raw_response)
    # print("#################################")
    # print(responseObj2.raw_response)

    # print(responseObj.raw_response)
    # print(responseObj.status)

    scraper(url, responseObj)
    print("TOTAL Unique links: " + str(len(uniquelinks)))
    print("FAILED LINKSSS: " + str(failedlinks))

    # print(resp)
    # print(resp.url)
    # print(test.json()['result'])