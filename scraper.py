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

# linkqueue = []
# uniquelinks = []
# failedlinks = []
# uniqueurls = set()
uniquepages = 0
commonwordsdict = dict()
subdomains = dict()
longestlength = 0
longesturl = ""
stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours     ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]


def scraper(url, resp):
    print(uniquepages)
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


def print_everything(num):
    global uniquepages, commonwordsdict, subdomains, longestlength, longesturl

    f = open("IMPORTANT_INFORMATION.txt", "w")
    f.write("Printing out for " + str(num) + " of links \n-----------------------\n")
    f.write("Number of unique pages: " + str(uniquepages) + "\n-----------------------\n")
    f.write("Longest page: " + longesturl + ", " + str(longestlength) + "\n-----------------------\n")
    sortedwords = sorted(commonwordsdict.items(), key=lambda x: x[1], reverse=True)
    f.write("Common words: \n")
    count = 0
    for tup in sortedwords:
        if count < 50:
            f.write(tup[0] + " = " + str(tup[1]) + '\n')
            count += 1
        else:
            break
    
    f.write("\n-----------------------\nSubdomains: \n")
    sorted_subdomains = sorted(subdomains.items())
    for tup in sorted_subdomains:
        f.write(tup[0] + ", " + str(tup[1]) + "\n")
    
    f.close()



def extract_next_links(url, input_response):
    global uniquepages, commonwordsdict, subdomains, longestlength, longesturl

    print("NOW EXTRACTING " + url)
    #print(longestlength)
    # Implementation requred.
    extracted_links = []

    if input_response == None:
        return []

    
    try:
        if 200 <= input_response.status_code < 400:
            pass
        elif input_response.status_code >= 400:
            print("Status code between 400 and 599")
            return []
    except:
        print("If you see this message then you're seriously stupid")


    txt = ""

    try:
        txt = input_response.raw_response.content
    except:
        print("No content in raw response")
        return []


    try:
        soup = BeautifulSoup(txt, "html.parser")


        #TOKENIZE
        text = soup.get_text()
        tokens = tokenize(text)
        if len(tokens) < 250:   # Checking for low content
            return []


        print(len(tokens))
        #print("LL: " ,longestlength)
        print("UP:", uniquepages)
        if len(tokens) > longestlength:
            longestlength = len(tokens)
            longesturl = url


        computeWordFrequencies(tokens)
        uniquepages += 1

         ####### SUBDOMAIN 
        subd = urlparse(url).netloc
        if subd in subdomains:
            subdomains[subd] += 1
        else:
            subdomains[subd] = 1




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
        # if parsed.netloc == "" and str(parsed.path)[0:len(
        #         "today.uci.edu/department/information_computer_sciences")] == "today.uci.edu/department/information_computer_sciences":
        #     return True

        if parsed.scheme not in set(["http", "https"]):
            return False


        if ("ics.uci.edu" in parsed.netloc or "cs.uci.edu" in parsed.netloc or "informatics.uci.edu" in parsed.netloc or "stat.uci.edu" in parsed.netloc) or (parsed.netloc == "" and str(parsed.path)[0:len("today.uci.edu/department/information_computer_sciences")] == "today.uci.edu/department/information_computer_sciences"):
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



# def get_response(url):
#     try:
#         resp = requests.get(url)
#         resp_dict = {'url': url, 'status': resp.status_code, 'response': pickle.dumps(resp.text.encode())}

#         return response.Response(resp_dict)
#     except:
#         print("Could not get response for URL")


# def similarity(l1, l2):
#     num = 0
#     for i in range(10):
#         if l1[i] == l2[i]:
#             num += 1
#     return num / 10


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
    global stopwords

    #freq_dict = {}
    for i in tokens:
        if i not in stopwords:
            if i in commonwordsdict.keys():
                commonwordsdict[i] += 1
            else:
                commonwordsdict[i] = 1
    #return freq_dict


if __name__ == '__main__':

    url = "https://www.ics.uci.edu/alumni/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/hall_of_fame/hall_of_fame/stayconnected/stayconnected/stayconnected/hall_of_fame/hall_of_fame/hall_of_fame/index.php"
    thingy = urlparse(url)
    print(thingy.path)

    # url = "https://www.stat.uci.edu"
    # resp = get_response(url)

    # #print(uniquepages)

    # # set_globals()

    # print(scraper(url, resp))
    
    # print_everything()

    # url = "http://www.vision.ics.uci.edu"
    # url2 = "https://www.cs.uci.edu"
    # url3 = "https://www.informatics.uci.edu"
    # url4 = "https://www.stat.uci.edu"

    # #urltest = "http://www.vision.ics.uci.edu"
    # urltest = "http://www.ics.uci.edu/about"


    # responseObj = get_response(url)
    # responseObj2 = get_response(url2)
    # responseObj3 = get_response(url3)
    # responseObj4 = get_response(url4)

    # scraper(url, responseObj)
    # scraper(url2, responseObj2)
    # scraper(url3, responseObj3)
    # scraper(url4, responseObj4)
    
    # print("TOTAL Unique links: " + str(len(uniquelinks)))
    # print("FAILED LINKSSS: " + str(failedlinks))

    # commonwordsdict = {'apple':78, 'banana':90, 'green':50, 'birthday':450, 'wassup':69, 'happy':2, 'peach':0}
    # subdomains = {'ics.com':5, 'google.com':101, 'asomething.gov':56}
    # print_everything()

    # responseObj = get_response(urltest)
    # scraper(urltest, responseObj)
