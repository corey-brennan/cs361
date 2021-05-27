import requests

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
            if r and r.status_code >= 200 and r.status_code < 300:
                
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