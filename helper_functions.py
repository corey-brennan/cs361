import pandas as pd
import concurrent.futures
import requests
import time

def calculate_grade(perc):

    perc = perc * 100 
    if perc >= 90:
        return('A')
    elif perc >= 80:
        return('B')
    elif perc >= 70:
        return('C')
    elif perc >= 60:
        return('D')
    else:
        return('F')

def calculate_article_health(urls):

    # Setting up variables
    working = [] # Holds working urls
    notWorking = [] # Holds non-working urls
    numWorking = 0 # Holdings number of working urls
    total = len(urls) # Total number of urls entered

    # Iterating through URLs
    for url in urls:
        
        # Checking to ensure url is appropriate type
        if type(url) == str:
            
            # Ensuring protocol is specified
            if url[0:7] != "http://" and url[0:8] != "https://":
                url = "https://" + url
            
            # Trying to request the url
            try:
                r = requests.get(url)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                notWorking.append(url)
                continue;
                
            # Checking if status code is appropriate
            if r and r.status_code >= 200 and r.status_code < 400:
                working.append(url)
                numWorking += 1
                
            else:
                notWorking.append(url)
        
        # If unexpected datatype, put into not working
        else:
            notWorking.append(url)

    # Creating result obj to return
    result = {
        'working' : working,
        'notWorking' : notWorking,
        'percentWorking' : numWorking/total,
        'grade' : calculate_grade(numWorking/total)
    }

    return result

# FUNCTION ADAPTED FROM https://stackoverflow.com/questions/2632520/what-is-the-fastest-way-to-send-100-000-http-requests-in-python
def calculate_article_health_threaded(urls):

    working = []
    notWorking = []
    numWorking = 0
    total = len(urls)
    CONNECTIONS = 1000
    TIMEOUT = 5
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"

    def load_url(url, timeout):
            
        # Ensuring protocol is specified
        original_url = url
        if url[0:7] != "http://" and url[0:8] != "https://":
            url = "https://" + url

        ans = requests.head(url, timeout=timeout, headers={'User-Agent': user_agent})
        return {"status_code": ans.status_code, "url": original_url}

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = {executor.submit(load_url, url, TIMEOUT): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as exc:
                data = {"status_code": 500, "url": future_to_url[future]}
            finally:
                if 200 <= data["status_code"] < 400:
                    working.append(data["url"])
                    numWorking += 1
                else:
                    notWorking.append(data["url"])

    # Creating result obj to return
    result = {
        'working' : working,
        'notWorking' : notWorking,
        'percentWorking' : numWorking/total,
        'grade' : calculate_grade(numWorking/total)
    }

    return result