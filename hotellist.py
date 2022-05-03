import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import concurrent.futures
import os


initialurl= "https://www.venuelook.com/Mumbai/Restaurants?area=mumbai&type=Restaurants&page="
linkurls=[f"{initialurl}{i}" for i in range(0,34)]


def hotelurl_list(url):
    ''' function for capturing the lonk of each hotel in the main url '''
    page=requests.get(url)
    soup = bs(page.content, 'html.parser')
    h2tag=soup.find_all('h2')
    links= [a.find("a")["href"] for a in h2tag if a.find("a") is not None]
    hotel_link_dict={'hotel_links':links}   
    hotel_df=pd.DataFrame(hotel_link_dict)
    #hotel_df= hotel_df.tail(1)
    if os.path.isfile("HOTEL_link.csv"):        
        
            hotel_df.to_csv("HOTEL_link.csv",index=False,header=False,mode='a')            
    else:
             hotel_df.to_csv("HOTEL_link.csv",index=False)
    print(f"{hotel_df} downloaded")

# running a thread to capture the links fast

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(hotelurl_list, linkurls)


df=pd.read_csv("HOTEL_link.csv")
hotellist=df['hotel_links'].tolist()


def hotellist_mumbai(url):
    hotel_name=[]
    address=[]
    mobile_number=[]

    page=requests.get(url)
    soup=bs(page.content,'html.parser')
    try:
        hotel_name.append(soup.find_all('h1',{'class':"vendor-details"})[0].text)
    except Exception:
        hotel_name.append(None)
    try:
        address.append(soup.find_all('p',{'class':"text-tertiary"})[0].text)
    except Exception:
        address.append(None)
    try:
        mobile_number.append(soup.find_all('a',{'class':"callhotline"})[0].text.strip())
    except Exception:   
        mobile_number.append(None)
    contact_dict1={'hotel_name':hotel_name,'address':address,'mobile_number':mobile_number}   
    
    hotel_df=pd.DataFrame(contact_dict1)
    #hotel_df= hotel_df.tail(1)    
    if os.path.isfile("HOTEL_FINAL.csv"):        
        
            hotel_df.to_csv("HOTEL_FINAL.csv",index=False,header=False,mode='a')            
    else:
             hotel_df.to_csv("HOTEL_FINAL.csv",index=False)
    
    
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(hotellist_mumbai, hotellist)  
