import requests
from bs4 import BeautifulSoup

def get_page(url: str):
    headers = {
        "Accept": "text/html, */*",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Origin": "www.yelp.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Host": "www.yelp.fr",
        "Referer": url,
        "Cookie": "bse=2b499f54fd7b45d3b26cb95b4c612115; wdi=2|1E5A5BFCF6079979|0x1.9684060b806a3p+30|a53a07cc29b39e2f; xcj=1|GxauDFSOw0dLkku9NIkIKEzhC2MFeoOWWDbhOFoOXcs; bsi=1%7Cf39fbf2a-468b-45ed-8f75-093bc3388400%7C1705068738926%7C1705068509210; pilot_spses.d161=*; pilot_spid.d161=595ca824-5c37-4a99-80dc-33c7132d30c5.1705068510.1.1705069107..ad7f273e-1887-42bb-bb4e-c6df5ad0c6e3..dc5426a7-89c9-464e-89ed-05b7e488c694.1705068509553.33; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jan+12+2024+15%3A12%3A21+GMT%2B0100+(heure+normale+d%E2%80%99Europe+centrale)&version=202307.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=8f50231f-f28f-4bd4-b1ce-de76f08acf1c&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&iType=2&geolocation=FR%3BGES&AwaitingReconsent=false; g_state={\"i_p\":1705075716132,\"i_l\":1}; OptanonAlertBoxClosed=2024-01-12T14:08:39.459Z", 
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "X-Requested-With": "XMLHttpRequest",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        html = response.text
    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return None
    
    if not html:
        print("No HTML received.")
        return None

    return html

def extract_reviews(html: str):
    soup = BeautifulSoup(html, "html.parser")

    reviews = []
    comments = soup.find_all("p", class_="comment__09f24__D0cxf css-qgunke")
    for comment in comments:
        spans = comment.find_all("span", class_=" raw__09f24__T4Ezm", lang="en")
        for span in spans:
            reviews.append(span.text)

    print(reviews)
    return reviews


if __name__ == "__main__":

    html = get_page("https://www.yelp.com/biz/olio-e-pi%C3%B9-new-york-7")
    if html is not None:
        reviews = extract_reviews(html)
        print(reviews)
    else:
        print("Failed to retrieve page.")

    print("Done.")