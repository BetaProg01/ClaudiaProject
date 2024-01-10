from collections import Counter
import requests
from bs4 import BeautifulSoup

def get_page_reduced_with_keywords(url: str, keyword: str):
    headers = {
        "Host": "www.tripadvisor.com",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "text/html, */*",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest",
        "X-Puid": "7b3f2595-c29f-4ebb-88fc-324122094744",
        "Origin": "https://www.tripadvisor.com",
        "Referer": url,
        "Connection": "keep-alive",
        "Cookie": "TADCID=lcxnhexjQULWydksABQCCKy0j55CTpGVsECjuwJMq3rC9X3jsPJr6-c7dMn3XbDgQUFlrinvdUE0n3CtNGB4v7YGI3hrA8PpdNg; TASameSite=1; TAUnique=%1%enc%3AHlUvYPZfLyB3joSkdX8suzDcHFPNnqbwpuSM%2FNTRpmeHZTAYYbtYqcK2%2Fd7EXXJhNox8JbUSTxk%3D; TASSK=enc%3AAFxaiJ%2FNz2aBIV42%2F1PQC3H5gLGJWKm5lhG9IaMbK9CkroTMrOhUbr8q1DjhILrrIuMLI2e5soK4mYrveU0GV9cV1blVhA56Ly3zNDfUzXKyiDYCwKmdxuy1QGEuYLlNRg%3D%3D; PAC=AFbbndDfjbuPgZZzYsn6uU9ItQx6ueWQRTn2_JjBD2U4tAy0oCXHSCJvXkfyti2Lsi6ZCNIGrHWjR9o9osnVbiT_q0nZqD65KQWawnkMBvGfApqN5J8LTDOSZLVv4ngBxbkml1DQIClXpzmBZ03mAvONz2Jz5X1cnxEv2O1us3KjPfC2NSOJMGCh3N6Yv5PzrbtqlI5ttZFNOAErsCW_W2xYQNeZXp0r3qI4B9m956D7; VRMCID=%1%V1*id.11607*llp.%2F-a_gclid%5C.CjwKCAiA1__2D__6sBhAoEiwArqlGPuPM3q__5F__Up01PNe__5F__UHxLeZ4gICF3k1WWPrn8sA__5F__GlZbigN5zbaqsh__5F__RoCiXQQAvD__5F__BwE-m11607-a_supac%5C.2060740055-a_supag%5C.10260201484-a_supai%5C.671602492052-a_supbk%5C.1-a_supcm%5C.179301124-a_supdv%5C.c-a_supli%5C.-a_suplp%5C.9055933-a_supnt%5C.g-a_supti%5C.kwd__2D__119671122*e.1705336823084; PMC=V2*MS.38*MD.20240108*LD.20240109; TART=%1%enc%3ApknDa4chFNZTY4yIoYquzdkYp30%2BA9kGkhT0B7Oi7XNDlytEN6Zb93jcHxGUHvLIG9xzEh4vPFU%3D; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*DSM.1704754259380*RS.1*RY.2024*RM.1*RD.9*RH.20*RG.2; TAUD=LA-1704732023084-1*RDD-1-2024_01_08*HDD-22236292-2024_01_21.2024_01_22*HC-80379311*VRC-80379312*RD-85200934-2024_01_09.1878682*LG-85203406-2.1.F.*LD-85203407-.....; _abck=46A7C6B63BB2D2A096219BA6B7AA6B86~-1~YAAQmeJIF8UH53mMAQAAQOy57gvq4Ow3n6ko0SyK8ry6eUMTqh/ml6B35KXC+aZ5DAW0TK8vvqGfKu0b2urxG9VRU/v9/nV7r9zqtOH/vcM5/SYnE8yqvTD1o9fHcUKHaWBnPqJqFu+kj/DapNdDKcx3V9rM5oLr1TW2ydW6dg2ayFMUus4uWyX05BsCGec5T7b3hQUj+Hoy9ekfXQWyNizsbKu+DYXsYUcwo9gkxctuylZw/WOJUMJwnVQTanj2QOeJQhrA0i7dvxHHKTwabq+W4J1t+EmKOLavu5eLqkMxXjzc6UdttwRhAA3j/xs1kgu4HOakEsPqOXqfFA7UztbYieqvBmB8lAkwIf5bvAyz0UWhn1TiolZkpi6fm8F2m1iHBrlX6pOp8+rqfouB~-1~-1~-1; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jan+09+2024+17%3A20%3A35+GMT%2B0100+(heure+normale+d%E2%80%99Europe+centrale)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=627466bc-15a5-4fce-99be-688f3d2fec7b&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A1%2CC0002%3A1%2CC0003%3A1%2CV2STACK42%3A1&geolocation=FR%3BGES&AwaitingReconsent=false; OptanonAlertBoxClosed=2024-01-08T16:40:37.807Z; eupubconsent-v2=CP4D8FgP4D8FgAcABBENAiEsAP_gAEPgACiQg1QoYAAgAEAAQAAwACIAFAAhABUAGQAOQAeACGAEgASwAnACgAFUALAAtABfADEAMoAaABqADmAHYAfABCgCIAIwASQAmABOACgAFWALQAtwBdAF-AMIAxQBkAGUANEAbABtADfAHIAc4A7gDxAIAAhYBEAEXAI4AjwBJwCVAJaATIBNgCdAFCAKQAVAArQBZQC4ALkAX0AwADBAGGAMcAZ0A0gDVgGuAbAA4IBxAHJAPEA84B8AHzAPsA_YB_gIBAQYBBwCIwEYARqAjgCOgEigJKAk0BLQEuAJgATgAnUBPQE_AKLAUgBSQCmgFZgK8Ar4BZgC4AFzALsAXkAvoBgQDFAGSAM1AZwBnQDQQGmAagA2gBtgDcAHCAO2Ad8A80B6gHrAPeAfIA-oB-4D_gQBAgQCBQEEgIMgQkBCcCFwIYAQ2AiKBEoETQIpAioBFgCLwEagI4AR2Aj0BIgCSwEqAJWgSyBLQCXgExAJlgTSBNQCbIE4gTlAnYCdwE_wKGAoiBRgFGwKQApEBScClgKXAU2AqIBUkCqQKqAVcArKBXwFfwLDAsWBZAFlALMAWeAtEBasC1wLYgW6Bb0C4QLigXKBc0C6ALugXkBecC9gL3gX6Bf0DAAMDAYyBFeCbIJvQTgBOEINQg1QWwAEQAKAAuABwAHgAVAAuABwADwAIAASAAvgBiAGUANAA1AB4AD8AIgATAAoABTACrAFsAXQAxABoADeAH4AQkAiACJAEcAJYATQAwABhgDLAGaANkAcgA-IB9gH7AP8BAACDgERgIsAjABGoCOAI6ASIAkoBPwCoAFzALyAX0AxQBnwDXgG0ANwAdIA7YB9gD_gImAReAj0BIgCVAErAJigTIBMoCZwE7AKHgUgBSICkwFNgKkAVVAsQCxQFlALRgWwBbIC3QFyALoAXaAu-BeQF5gL6AYJBNsE3IJvAm-BOEINQBQIAQADoALgA2QCIAGEAToAuQCBwQAMADoAVwBEADCAJ0AgcGADgA6AC4ANkAiABhAFyAQOEABwAdADZAIgAYQBOgC5AIHCgAYAXADCAQOGAAwBXAGEAgcOADgA6AFcARAAwgCdAIHARXIAAgDCAQOJAAwCIAGEAgcUACgA6AIgAYQBOgEDgAAA.f_wACHwAAAAA; OTAdditionalConsentString=1~43.46.55.61.70.83.89.93.108.117.122.124.135.136.143.144.147.149.159.192.196.202.211.228.230.239.259.266.286.291.311.317.320.322.323.327.338.367.371.385.394.397.407.413.415.424.430.436.445.453.482.486.491.494.495.522.523.540.550.559.560.568.574.576.584.587.591.737.802.803.820.821.839.864.899.904.922.931.938.979.981.985.1003.1027.1031.1040.1046.1051.1053.1067.1085.1092.1095.1097.1099.1107.1135.1143.1149.1152.1162.1166.1186.1188.1201.1205.1215.1226.1227.1230.1252.1268.1270.1276.1284.1290.1301.1307.1312.1345.1356.1364.1365.1375.1403.1415.1416.1421.1440.1449.1455.1495.1512.1516.1525.1540.1548.1555.1558.1570.1577.1579.1583.1584.1591.1603.1616.1638.1651.1653.1667.1677.1678.1682.1697.1699.1703.1712.1716.1721.1725.1732.1745.1750.1765.1769.1782.1786.1800.1810.1825.1827.1832.1838.1840.1842.1843.1845.1859.1866.1870.1878.1880.1889.1899.1917.1929.1942.1944.1962.1963.1964.1967.1968.1969.1978.2003.2007.2008.2027.2035.2039.2047.2052.2056.2064.2068.2072.2074.2088.2090.2103.2107.2109.2115.2124.2130.2133.2135.2137.2140.2145.2147.2150.2156.2166.2177.2183.2186.2205.2213.2216.2219.2220.2222.2225.2234.2253.2279.2282.2292.2299.2305.2309.2312.2316.2322.2325.2328.2331.2334.2335.2336.2337.2343.2354.2357.2358.2359.2370.2376.2377.2387.2392.2400.2403.2405.2407.2411.2414.2416.2418.2425.2440.2447.2461.2462.2465.2468.2472.2477.2481.2484.2486.2488.2493.2498.2499.2501.2510.2517.2526.2527.2532.2535.2542.2552.2563.2564.2567.2568.2569.2571.2572.2575.2577.2583.2584.2596.2604.2605.2608.2609.2610.2612.2614.2621.2628.2629.2633.2636.2642.2643.2645.2646.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2687.2690.2695.2698.2713.2714.2729.2739.2767.2768.2770.2772.2784.2787.2791.2792.2798.2801.2805.2812.2813.2816.2817.2821.2822.2827.2830.2831.2834.2838.2839.2844.2846.2849.2850.2852.2854.2860.2862.2863.2865.2867.2869.2873.2874.2875.2876.2878.2880.2881.2882.2883.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2913.2914.2916.2917.2918.2919.2920.2922.2923.2927.2929.2930.2931.2940.2941.2947.2949.2950.2956.2958.2961.2963.2964.2965.2966.2968.2973.2975.2979.2980.2981.2983.2985.2986.2987.2994.2995.2997.2999.3000.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3024.3025.3028.3034.3037.3038.3043.3048.3052.3053.3055.3058.3059.3063.3066.3068.3070.3073.3074.3075.3076.3077.3078.3089.3090.3093.3094.3095.3097.3099.3104.3106.3109.3112.3117.3119.3126.3127.3128.3130.3135.3136.3145.3150.3151.3154.3155.3163.3167.3172.3173.3182.3183.3184.3185.3187.3188.3189.3190.3194.3196.3209.3210.3211.3214.3215.3217.3219.3222.3223.3225.3226.3227.3228.3230.3231.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3296.3299.3300.3306.3307.3314.3315.3316.3318.3324.3327.3328.3330.3331.3531.3731.3831.3931.4131.4531.4631.4731.4831.5031.5231.6931.7031.7235.7831.7931.8931.9731.10231.10631.10831.11031.11531.12831.13632.13731.14237.16831; TATrkConsent=eyJvdXQiOiJTT0NJQUxfTUVESUEiLCJpbiI6IkFEVixBTkEsRlVOQ1RJT05BTCJ9; ab.storage.sessionId.6e55efa5-e689-47c3-a55b-e6d7515a6c5d=%7B%22g%22%3A%222850cd99-2894-e68b-c2c4-cc0ce5997927%22%2C%22e%22%3A1704812482733%2C%22c%22%3A1704812421767%2C%22l%22%3A1704812422733%7D; ab.storage.deviceId.6e55efa5-e689-47c3-a55b-e6d7515a6c5d=%7B%22g%22%3A%22277a957b-0cc9-a139-a38d-a45bf6e6d952%22%2C%22c%22%3A1704732038132%2C%22l%22%3A1704812421768%7D; pbjs_sharedId=0f7d47b1-6eb0-49f4-854c-c3db8e0369a1; pbjs_sharedId_cst=5ywrLGIsCA%3D%3D; _lr_sampling_rate=100; _lr_env_src_ats=false; pbjs_unifiedID=%7B%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-01-08T16%3A40%3A38%22%7D; pbjs_unifiedID_cst=5ywrLGIsCA%3D%3D; TALanguage=ALL; TASession=V2ID.31892C771C724E0AAEB0FB2BDD8FDAAA*SQ.218*LS.DemandLoadAjax*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.ALL*FA.1*DF.0*FLO.1878682*TRA.false*LD.1878682*EAU._; ServerPool=B; TAReturnTo=%1%%2FRestaurant_Review-g60763-d1878682-Reviews-Olio_e_Piu-New_York_City_New_York.html; bm_sz=1DC4E150A86C1ACD8CA390317680BF93~YAAQmeJIF8YH53mMAQAAQOy57hb9zihNLTW8sO1n6i4EGuX8aMsRu2D3O5jVsO3sT4mviPegOA4IoZ3Ld0wZZe4TU4OYNzaN7rtXQ7R+kP+NXFsiLhL++SY4UPkFiM1SqWPEZ7kFPM6w7bdruu1MyeqFYljyFM9SF+CsFm85mRIgO2fp07b36xVtjlpxlCk2UVreFmK+kqPAjVSOO/OG04k7mSvcCxL+QMcpgm9DCdPpqzUGXMCHjX0bu6tlM9C79Jcbwn7vvaLHI0n8u93GiLthUoB6ZThzmdteDBxswCzroS/gi7N/+g==~3621168~3293509; __vt=AxlKhD4_vmZ2fT1jABQCCQPEFUluRFmojcP0P3EgGiqmITe0cOxl5MSAHY1EclZ2XA-v7qKjyDP4Yzgv4M-uCP5TyLb7cXBKQ-yMoILRhA_K442yDyjZk-oTkNFiGZSe8uvnrksVJC64hHX27GD1Biggvg; SRT=TART_SYNC; TASID=31892C771C724E0AAEB0FB2BDD8FDAAA; roybatty=TNI1625!APUsL3hUGzvSzYopkJtWiVx0ACb7PZWT1N9SStKuM1JtIG3u6UAVxKdLNW9uwsgqrGRan05qQzy64lybOOfJgQm%2BJbZI%2FZvTTPvHIz3Az9fMo1SXrYU7E5YPiP3fFDg0nz7B%2BP%2FPZtENOlmjF%2FGxWJJ22c3AUkb3%2FPPxFWm0PFs4GK2U51b12Kb7afkHinu%2BoQ%3D%3D%2C1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }
    data = {
        "sortType": "most_recent",
        "preferFriendReviews": "FALSE",
        "t": "",
        "q": keyword,
        "filterSeasons": "",
        "filterLang": "ALL",
        "filterSafety": "FALSE",
        "filterSegment": "",
        "trating": "",
        "reqNum": "1",
        "isLastPoll": "false",
        "changeSet": "REVIEW_LIST",
        "puid": "7b3f2595-c29f-4ebb-88fc-324122094744"
    }
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return None
    
def get_review_ids(html, existing_ids):
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    review_containers = soup.find_all('div', class_='reviewSelector')
    review_ids = []
    for container in review_containers:
        review_id = container.get('data-reviewid')
        if review_id is None:
            print(f'Missing data-reviewid: {container}')
        elif review_id not in existing_ids:
            review_ids.append(review_id)
    return review_ids


def get_all_reviews_page(ids):
    url = "https://www.tripadvisor.com/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS_RESP&metaReferer="
    
    headers = {
        "Host": "www.tripadvisor.com",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "X-Puid": "b3de220c-f631-4ddf-bd72-c906203fa7d8",
        "Content-Length": "4681",
        "Origin": "https://www.tripadvisor.com",
        "Connection": "keep-alive",
        "Referer": "https://www.tripadvisor.com/Restaurant_Review-g60763-d1878682-Reviews-Olio_e_Piu-New_York_City_New_York.html",
        "Cookie": "TADCID=TLDfN77InywTBfEtABQCCKy0j55CTpGVsECjuwJMq3rIqsOtfDafla1fxpxgLF741YJckfqRyU1O1nZeaLkqtbNBDOdP_YhzXHQ; TASameSite=1; TAUnique=%1%enc%3AHlUvYPZfLyB3joSkdX8suzDcHFPNnqbwpuSM%2FNTRpmeHZTAYYbtYqcK2%2Fd7EXXJhNox8JbUSTxk%3D; TASSK=enc%3AAFxaiJ%2FNz2aBIV42%2F1PQC3H5gLGJWKm5lhG9IaMbK9CkroTMrOhUbr8q1DjhILrrIuMLI2e5soK4mYrveU0GV9cV1blVhA56Ly3zNDfUzXKyiDYCwKmdxuy1QGEuYLlNRg%3D%3D; PAC=ADeAJ_4rpOYHCVNbV8YIC2r-d0trjdT4ouO6bLZPpVJ64wi-dMjUOwVVJUlGHFz17o407A0x2swMOZWIUuVEx6nArmZ285VXP7ZEGe1QVO11sf-BaiA1boR7JHp9kfqWPtv_5MrliiqHg0ilFnj-m7FgCSSTWbPVkEra6R8H0uDizWWHPnWfjC_Z3dJ2s56aRTQvBs3yLtAqWZMp7siGzokTPE8wIcPpWNuByf7iNbTk; VRMCID=%1%V1*id.11607*llp.%2F-a_gclid%5C.CjwKCAiA1__2D__6sBhAoEiwArqlGPuPM3q__5F__Up01PNe__5F__UHxLeZ4gICF3k1WWPrn8sA__5F__GlZbigN5zbaqsh__5F__RoCiXQQAvD__5F__BwE-m11607-a_supac%5C.2060740055-a_supag%5C.10260201484-a_supai%5C.671602492052-a_supbk%5C.1-a_supcm%5C.179301124-a_supdv%5C.c-a_supli%5C.-a_suplp%5C.9055933-a_supnt%5C.g-a_supti%5C.kwd__2D__119671122*e.1705336823084; PMC=V2*MS.38*MD.20240108*LD.20240110; TART=%1%enc%3ApknDa4chFNZTY4yIoYquzdkYp30%2BA9kGkhT0B7Oi7XNDlytEN6Zb93jcHxGUHvLIG9xzEh4vPFU%3D; TATravelInfo=V2*AY.2024*AM.1*AD.21*DY.2024*DM.1*DD.22*A.2*MG.-1*HP.2*FL.3*DSM.1704821440245*RS.1*RY.2024*RM.1*RD.10*RH.20*RG.2; TAUD=LA-1704732023084-1*RDD-1-2024_01_08*HC-80379311*VRC-80379312*HDD-89417090-2024_01_21.2024_01_22*RD-164327715-2024_01_10.1878682*LD-164328559-2024.1.21.2024.1.22*LG-164328561-2.1.F.; _abck=46A7C6B63BB2D2A096219BA6B7AA6B86~-1~YAAQmeJIFyH2/HmMAQAA2aO98ws59W5cVtD1MTrAQWoGCDhZeQ2u5vHkLNWWEyakgVyiALN8EndCOjN71fN0b4yb/AyliXJfsjpGOFpk7uCnecMwcOTOJNKxnkUiSiPSeivbbx6m+BKhfZ3E2qjXgnbkgX5YA9c9dkHVg04e65s6+Rwt5S/8S+nYIiqJYhrgZkfaA8jg3SEG7HdvwX3p7WQzBdArITZuJyEyPZGmquSEnN7PeAbUgj6tmV/hD6VRbUMbEG/T9iqcZ+Z1JJJicq57z9Z5xVet8JESQCyy6Tz9hudaIbs72KRlPA9qmJcniVN9sAG9dpNeGLiD2+PiVqR+KTD/FCrpFEf/C/SjUlvSUEW0TAwv3xIaGswzHePTI9cvSEW7olezRaAQ2Alx~-1~-1~-1; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jan+10+2024+15%3A19%3A22+GMT%2B0100+(heure+normale+d%E2%80%99Europe+centrale)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=627466bc-15a5-4fce-99be-688f3d2fec7b&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A1%2CC0002%3A1%2CC0003%3A1%2CV2STACK42%3A1&geolocation=FR%3BGES&AwaitingReconsent=false; OptanonAlertBoxClosed=2024-01-08T16:40:37.807Z; eupubconsent-v2=CP4D8FgP4D8FgAcABBENAiEsAP_gAEPgACiQg1QoYAAgAEAAQAAwACIAFAAhABUAGQAOQAeACGAEgASwAnACgAFUALAAtABfADEAMoAaABqADmAHYAfABCgCIAIwASQAmABOACgAFWALQAtwBdAF-AMIAxQBkAGUANEAbABtADfAHIAc4A7gDxAIAAhYBEAEXAI4AjwBJwCVAJaATIBNgCdAFCAKQAVAArQBZQC4ALkAX0AwADBAGGAMcAZ0A0gDVgGuAbAA4IBxAHJAPEA84B8AHzAPsA_YB_gIBAQYBBwCIwEYARqAjgCOgEigJKAk0BLQEuAJgATgAnUBPQE_AKLAUgBSQCmgFZgK8Ar4BZgC4AFzALsAXkAvoBgQDFAGSAM1AZwBnQDQQGmAagA2gBtgDcAHCAO2Ad8A80B6gHrAPeAfIA-oB-4D_gQBAgQCBQEEgIMgQkBCcCFwIYAQ2AiKBEoETQIpAioBFgCLwEagI4AR2Aj0BIgCSwEqAJWgSyBLQCXgExAJlgTSBNQCbIE4gTlAnYCdwE_wKGAoiBRgFGwKQApEBScClgKXAU2AqIBUkCqQKqAVcArKBXwFfwLDAsWBZAFlALMAWeAtEBasC1wLYgW6Bb0C4QLigXKBc0C6ALugXkBecC9gL3gX6Bf0DAAMDAYyBFeCbIJvQTgBOEINQg1QWwAEQAKAAuABwAHgAVAAuABwADwAIAASAAvgBiAGUANAA1AB4AD8AIgATAAoABTACrAFsAXQAxABoADeAH4AQkAiACJAEcAJYATQAwABhgDLAGaANkAcgA-IB9gH7AP8BAACDgERgIsAjABGoCOAI6ASIAkoBPwCoAFzALyAX0AxQBnwDXgG0ANwAdIA7YB9gD_gImAReAj0BIgCVAErAJigTIBMoCZwE7AKHgUgBSICkwFNgKkAVVAsQCxQFlALRgWwBbIC3QFyALoAXaAu-BeQF5gL6AYJBNsE3IJvAm-BOEINQBQIAQADoALgA2QCIAGEAToAuQCBwQAMADoAVwBEADCAJ0AgcGADgA6AC4ANkAiABhAFyAQOEABwAdADZAIgAYQBOgC5AIHCgAYAXADCAQOGAAwBXAGEAgcOADgA6AFcARAAwgCdAIHARXIAAgDCAQOJAAwCIAGEAgcUACgA6AIgAYQBOgEDgAAA.f_wACHwAAAAA; OTAdditionalConsentString=1~43.46.55.61.70.83.89.93.108.117.122.124.135.136.143.144.147.149.159.192.196.202.211.228.230.239.259.266.286.291.311.317.320.322.323.327.338.367.371.385.394.397.407.413.415.424.430.436.445.453.482.486.491.494.495.522.523.540.550.559.560.568.574.576.584.587.591.737.802.803.820.821.839.864.899.904.922.931.938.979.981.985.1003.1027.1031.1040.1046.1051.1053.1067.1085.1092.1095.1097.1099.1107.1135.1143.1149.1152.1162.1166.1186.1188.1201.1205.1215.1226.1227.1230.1252.1268.1270.1276.1284.1290.1301.1307.1312.1345.1356.1364.1365.1375.1403.1415.1416.1421.1440.1449.1455.1495.1512.1516.1525.1540.1548.1555.1558.1570.1577.1579.1583.1584.1591.1603.1616.1638.1651.1653.1667.1677.1678.1682.1697.1699.1703.1712.1716.1721.1725.1732.1745.1750.1765.1769.1782.1786.1800.1810.1825.1827.1832.1838.1840.1842.1843.1845.1859.1866.1870.1878.1880.1889.1899.1917.1929.1942.1944.1962.1963.1964.1967.1968.1969.1978.2003.2007.2008.2027.2035.2039.2047.2052.2056.2064.2068.2072.2074.2088.2090.2103.2107.2109.2115.2124.2130.2133.2135.2137.2140.2145.2147.2150.2156.2166.2177.2183.2186.2205.2213.2216.2219.2220.2222.2225.2234.2253.2279.2282.2292.2299.2305.2309.2312.2316.2322.2325.2328.2331.2334.2335.2336.2337.2343.2354.2357.2358.2359.2370.2376.2377.2387.2392.2400.2403.2405.2407.2411.2414.2416.2418.2425.2440.2447.2461.2462.2465.2468.2472.2477.2481.2484.2486.2488.2493.2498.2499.2501.2510.2517.2526.2527.2532.2535.2542.2552.2563.2564.2567.2568.2569.2571.2572.2575.2577.2583.2584.2596.2604.2605.2608.2609.2610.2612.2614.2621.2628.2629.2633.2636.2642.2643.2645.2646.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2687.2690.2695.2698.2713.2714.2729.2739.2767.2768.2770.2772.2784.2787.2791.2792.2798.2801.2805.2812.2813.2816.2817.2821.2822.2827.2830.2831.2834.2838.2839.2844.2846.2849.2850.2852.2854.2860.2862.2863.2865.2867.2869.2873.2874.2875.2876.2878.2880.2881.2882.2883.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2913.2914.2916.2917.2918.2919.2920.2922.2923.2927.2929.2930.2931.2940.2941.2947.2949.2950.2956.2958.2961.2963.2964.2965.2966.2968.2973.2975.2979.2980.2981.2983.2985.2986.2987.2994.2995.2997.2999.3000.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3024.3025.3028.3034.3037.3038.3043.3048.3052.3053.3055.3058.3059.3063.3066.3068.3070.3073.3074.3075.3076.3077.3078.3089.3090.3093.3094.3095.3097.3099.3104.3106.3109.3112.3117.3119.3126.3127.3128.3130.3135.3136.3145.3150.3151.3154.3155.3163.3167.3172.3173.3182.3183.3184.3185.3187.3188.3189.3190.3194.3196.3209.3210.3211.3214.3215.3217.3219.3222.3223.3225.3226.3227.3228.3230.3231.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3296.3299.3300.3306.3307.3314.3315.3316.3318.3324.3327.3328.3330.3331.3531.3731.3831.3931.4131.4531.4631.4731.4831.5031.5231.6931.7031.7235.7831.7931.8931.9731.10231.10631.10831.11031.11531.12831.13632.13731.14237.16831; TATrkConsent=eyJvdXQiOiJTT0NJQUxfTUVESUEiLCJpbiI6IkFEVixBTkEsRlVOQ1RJT05BTCJ9; ab.storage.sessionId.6e55efa5-e689-47c3-a55b-e6d7515a6c5d=%7B%22g%22%3A%22791f390c-7526-1536-838b-116369ab23e8%22%2C%22e%22%3A1704896423795%2C%22c%22%3A1704896363782%2C%22l%22%3A1704896363795%7D; ab.storage.deviceId.6e55efa5-e689-47c3-a55b-e6d7515a6c5d=%7B%22g%22%3A%22277a957b-0cc9-a139-a38d-a45bf6e6d952%22%2C%22c%22%3A1704732038132%2C%22l%22%3A1704896363783%7D; pbjs_sharedId=0f7d47b1-6eb0-49f4-854c-c3db8e0369a1; pbjs_sharedId_cst=5ywrLGIsCA%3D%3D; _lr_env_src_ats=false; pbjs_unifiedID=%7B%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-01-08T16%3A40%3A38%22%7D; pbjs_unifiedID_cst=5ywrLGIsCA%3D%3D; TALanguage=ALL; TASession=V2ID.27620577FCFE42EF9FAB618EBAC30684*SQ.328*LS.DemandLoadAjax*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.ALL*FA.1*DF.0*FLO.1878682*TRA.false*LD.1878682*EAU._; ServerPool=B; TAReturnTo=%1%%2FRestaurant_Review-g60763-d1878682-Reviews-Olio_e_Piu-New_York_City_New_York.html; __vt=Jx7k9-ZUpo-srm4RABQCCQPEFUluRFmojcP0P3EgGiqrR6JVpwCOps2J4D2NFvNambY8tGJ6QSlJIBI2qqEDmyd-_dqG13Cgzqv8FWi52J_HkgHLYRSdZHdkgP6lefq4b9zuGL0wMyGl9y_U558z_M2i6g; SRT=TART_SYNC; TASID=27620577FCFE42EF9FAB618EBAC30684; bm_sz=51145E16AF3510BFC693C58AB4AC9224~YAAQmeJIFyL2/HmMAQAA2aO98xafmG2b/OolcpoxxBhUlag2ewb6pMfp5OHPC7kwxYjRv3KM/VeEAOfgu0BktGxRtatbPQYrCHZ17a0i5GIS1Uq+7jt1WZ+r/mf1ibuOl5PDDjAvqOIOQbiTVP1etu6zPVczQHZrOf0n3jHlIjlLpE4ZTwmYnfN6YHL8J2hKFiIj0fVZLkjcPPik8Gs06Bub7GA/o46iMvskJ9w34bp9FAXIHFGCFlGYzzpC9HThm5i8CY0W4xpsjcy4NTUNCstVqrBpIYdASfVXknP7dsLLVQxbgHjEyw==~3486769~3425333; roybatty=TNI1625!AD7jRB%2Fy%2FXygaGyD6fCTGoUmG712SCA8zVk3%2BlJC6ITDfwc4CPD%2FgBE9m2O0eWjOEAh5KKT0iaMeCXlLWCGX6hjX%2Ftt3fWyuyendGrZx1HwKH1I%2FHAieIcnvVuaca4VHEKN7mdIbukqZQn5774GDhZHvCcLxJ3gXBx9rqicj%2FpgSMNx3AHlXneYyY8OojQFqxg%3D%3D%2C1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }
    
    data = {
        "reviews": ",".join(ids)
    }
    response = requests.post(url, headers=headers, data=data)
    
    return response.text

def extract_review_text(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Find p elements that are not descendants of unwanted div elements
    review_elements = [p for p in soup.find_all('p', class_='partial_entry') 
                       if not any('mgrRspnInline' in parent.get('class', []) for parent in p.parents)]

    reviews = []
    for element in review_elements:
        review_text = element.text
        if review_text is not None:
            reviews.append(review_text)
        else:
            print(f'Missing review text: {element}')
    return reviews

def get_first_review_test():
    url = "https://www.tripadvisor.com/Restaurant_Review-g60763-d1878682-Reviews-Olio_e_Piu-New_York_City_New_York.html"
    html = get_page_reduced_with_keywords(url, "water")
    review_ids = get_review_ids(html)
    print(f"Ids : {review_ids}")
    full_reviews = get_all_reviews_page(review_ids)
    print(f"HTML : {full_reviews}")
    reviews = extract_review_text(full_reviews)
    print(reviews[0])
    
def count_bad_words():
    
    bad_words = ['Organic', 'Natural', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Herb', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Balanced', 'Holistic', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Farm-to-table', 'Unprocessed', 'Nutrient-rich', 'Holistic', 'Organic', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Holistic', 'Organic', 'Natural', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Holistic', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Holistic', 'Organic', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Farm-to-table', 'Unprocessed', 'Nutrient-rich', 'Balanced', 'Holistic', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Farm-to-table', 'Unprocessed', 'Nutrient-rich', 'Holistic', 'Natural', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Herb', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Balanced', 'Holistic', 'Organic', 'Natural', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Herb', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Local', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Balanced', 'Holistic', 'Green', 'Organic', 'Natural', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Farm-to-table', 'Unprocessed', 'Nutrient-rich', 'Holistic', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Holistic', 'Organic', 'Natural', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Holistic', 'Organic', 'Natural', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Herb', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Whole foods', 'Farm-to-table', 'Unprocessed', 'Nutrient-rich', 'Balanced', 'Holistic', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Unprocessed', 'Nutrient-rich', 'Holistic', 'Organic', 'Natural', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Herb', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Whole foods', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Balanced', 'Holistic', 'Green', 'Organic', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Herb', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Balanced', 'Holistic', 'Green', 'Organic', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Herb', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Balanced', 'Holistic', 'Green', 'Organic', 'Natural', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Herb', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Whole foods', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Balanced', 'Holistic', 'Organic', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Herb', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Balanced', 'Holistic', 'Green', 'Organic', 'Natural', 'GMO', 'Genetically', 'genetics', 'Chemical', 'Pesticide', 'Pest', 'Herbicide', 'Herb', 'Synthetic', 'Non-synthetic', 'Eco-friendly', 'Green farming', 'Clean farming', 'Environmentally', 'Earth-friendly', 'Sustainable', 'Eco-conscious', 'Health-conscious', 'toxic', 'additives', 'farming', 'eco-sensitive', 'Ecological', 'Chemical', 'Agroecological', 'Agro-organic', 'Eco-cultivated', 'Greenhouse gas', 'carbon footprint', 'Earth-conscious', 'Soil-friendly', 'Eco-harmonious', 'Health', 'Whole foods', 'Farm-to-table', 'Pure', 'Unprocessed', 'Nutrient-rich', 'Balanced', 'Holistic', 'Green']
    # Count the occurrences of each word
    word_counts = Counter(bad_words)

    # Get the words and counts sorted by count
    sorted_word_counts = word_counts.most_common()

    # Print the words and counts
    print(sorted_word_counts)

if __name__ == "__main__":
    
    #get_first_review_test()
    
    URLfile = "tripadvisorRestaurants.txt"
    keyword_file = "keywords_organic.txt"
    
    # Reset the reviews.txt file
    with open("reviews.txt", "w") as f:
        pass

    # Read the keywords from the file
    with open(keyword_file, "r") as f:
        keywords = [line.strip() for line in f]

    # Search the urls in the file tripadvisorRestaurants.txt
    with open(URLfile, "r") as f:
        urls = f.readlines()

    all_review_ids = []
    bad_words = []
    for url in urls:
        url = url.strip()
        print(f"Scraping {url}")
        for keyword in keywords:
            print(f"Searching for keyword: {keyword}")
            review_ids = get_review_ids(get_page_reduced_with_keywords(url, keyword), all_review_ids)
            if review_ids is not None:
                print(f"Found {len(review_ids)} review IDs for keyword {keyword}.")
                all_review_ids.extend(review_ids)
                if len(review_ids) < 2:
                    bad_words.append(keyword)
            else:
                print(f"No review IDs found for keyword {keyword}.")

    if all_review_ids:
        print(f"Extracting reviews for {len(all_review_ids)} IDs.")
        full_reviews = get_all_reviews_page(all_review_ids)
        reviews = extract_review_text(full_reviews)
        # Append the reviews to the file reviews.txt
        with open("reviews.txt", "a") as f:
            for review in reviews:
                f.write(review + "\n")
    else:
        print("No review IDs found.")
    print("Bad words: ", bad_words)
    print("Done.")

    #count_bad_words()