from tkinter import Tk
import pafy
from pydub import AudioSegment
import os
import urllib3
from bs4 import BeautifulSoup
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json
import urllib
from urllib.request import urlopen
from urllib.parse import urljoin
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error



def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        # log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    # print(e)


def getYouTubeUrl(query):
    # classic youtube search
    url = "https://www.youtube.com/results?search_query=" + query
    html = simple_get(url)
    soup = BeautifulSoup(html,"lxml")
    urlLists = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        if not vid['href'].startswith("https://googleads.g.doubleclick.net/"):
            urlLists.append('https://www.youtube.com' + vid['href'])
    if(len(urlLists) > 0):
        return urlLists[0]
    return None

# r = Tk()
# r.withdraw()
def getAudioClip():
    songName = input("Please enter the name of the song: ")
    scrapeImage(songName,os.getcwd())
    result = getYouTubeUrl(songName)

    while result == None:
        songName = input("Error: Please type the song differently: ")
        result = getYouTubeUrl(songName)
    return result

def get_soup(url,header):
    return BeautifulSoup(requests.get(url,headers=header).text,'html.parser')

def scrapeImage(query, save_directory, output='.img.jpg'):
    image_type="Action"
    query = query + " album art"
    query= query.split()
    query='+'.join(query)
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header)
    # print(soup)
    ActualImages=[]# contains the link for Large original images, type of  image
    for a in soup.find_all("div",{"class":"rg_meta"}):
        link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        ActualImages.append((link,Type))
    for img, Type in ActualImages:
            try:
                raw_img = urlopen(img).read()
                f = open(os.path.join(save_directory , output), 'wb')
                f.write(raw_img)
                f.close()
                break

                if not imghdr.what(os.path.join(save_directory, output)) == None:
                    break
                else:
                    os.remove(os.path.join(save_directory, output))
            except Exception as e:
                #print("could not load : "+img)
                #print(e)
                None

def load_image_inMP3(filename):
    print("hi")
    audio = MP3(filename+".mp3")
    audio.tags.add(
        APIC(
            encoding=3, # 3 is for utf-8
            mime='image/jpeg', # image/jpeg or image/png
            type=3, # 3 is for the cover image
            desc=u'Cover',
            data=open('.img.jpg','rb').read()
            )
    )
    audio.save()



# result = r.clipboard_get()
flag = 0
result = getAudioClip()
if result != None:
    qual=input("Hit 1 for best clarity, 2 for worst, 3 for other: ")
    qual=int(qual)
    if qual==3:
    	flag=1
    c=0
    url = result
    video = pafy.new(url)
    best = video.audiostreams
    for b in best:
    	print (str(c)+ " " + str(b))
    	c+=1;
    if flag==1:
    	index=input("Enter index")
    	index=int(index)
    elif qual==2:
    	index=c-1
    elif qual==1:
    	index=0

    filename = video.audiostreams[index]
    print (filename)

    x=filename.download(filepath=filename.title + "." + filename.extension)
    print("Current File Name is " + filename.title + " Would you like to change it\n")
    ans = input("Press 1 if you would like to change it else Press 0: ")
    ans = int(ans)
    if ans == 1:
        newTitle = input("Enter new title: ")
    print("Converting to MP3...\n")
    if ans == 1:
        AudioSegment.from_file(filename.title + "." + filename.extension).export("/Users/Parth/funProjects/"+newTitle + ".mp3", format="mp3")
    if ans == 0:
        AudioSegment.from_file(filename.title + "." + filename.extension).export("/Users/Parth/funProjects/"+filename.title + ".mp3", format="mp3")
    load_image_inMP3(filename.title)
    print("Deleting old File...\n")
    os.remove("/Users/Parth/funProjects/"+filename.title + "." + filename.extension)
    os.remove("/Users/Parth/funProjects/.img.jpg")

    print("Done!\n")
