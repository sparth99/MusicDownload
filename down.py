from tkinter import Tk
import pafy
from pydub import AudioSegment
import os
import urllib3
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup



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

flag = 0
# result = r.clipboard_get()
songName = input("Please enter the name of the song: ")
result = getYouTubeUrl(songName)

while result == None:
    songName = input("Error: Please type the song differently: ")
    result = getYouTubeUrl(songName)

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
    print("Deleting old File...\n")
    os.remove("/Users/Parth/funProjects/"+filename.title + "." + filename.extension)
    print("Done!\n")
