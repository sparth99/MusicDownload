from tkinter import *
from tkinter import ttk
from down import *

download_succesful = False
def guiMain(*args):
        songName = songNamee.get()
        flag = 0
        result = getAudioClip(songName)
        if result != None:
            url = result
            video = pafy.new(url)
            best = video.audiostreams
            filename = video.audiostreams[0]

            x=filename.download(filepath=filename.title + "." + filename.extension)

            print("Converting to MP3...\n")

            AudioSegment.from_file(filename.title + "." + filename.extension).export("/Users/Parth/funProjects/"+filename.title + ".mp3", format="mp3")
            metaData = getMetaData(songName)
            artist = metaData['artistName']
            title = metaData['trackName']
            if metaData['collectionName']:
                album = metaData['collectionName']
            else:
                album = 'none'
            load_image_inMP3(filename.title, artist, title, album)
            print("Deleting old File...\n")

            os.remove("/Users/Parth/funProjects/"+filename.title + "." + filename.extension)
            os.remove("/Users/Parth/funProjects/.img.jpg")
            os.rename("/Users/Parth/funProjects/"+filename.title + ".mp3","/Users/Parth/funProjects/"+title + ".mp3"  )
            print("Done")
            download_succesful = True



root = Tk()
root.title("Music Download")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

songNamee = StringVar()

ttk.Label(mainframe, textvariable="Enter the Song Here:").grid(column=2, row=2, sticky=(W, E))
feet_entry = ttk.Entry(mainframe, width=20, textvariable=songNamee)
feet_entry.grid(column=2, row=2, sticky=(W, E))


Button(mainframe, text="Download", command=guiMain).grid(column=3, row=3, sticky=W)
ttk.Label(mainframe, text="Enter Song Here:").grid(column=2, row=1, sticky=W)

if download_succesful:
    ttk.Label(mainframe, text="Download Succesful").grid(column=1, row=3, sticky=W)
    download_succesful = False



for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', guiMain)

root.mainloop()
