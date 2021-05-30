from tkinter import *
from tkinter import ttk
from pytube import YouTube
import os,requests
from PIL import ImageTk,Image


#Get Current Path or Script Path where Video will be Downloaded
try:
    PATH = os.path.dirname(os.path.abspath(__file__))
except NameError:
    PATH = os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd())))

window = Tk()
window.title('Youtube Downloader')
window.geometry('400x600+100+100')
url = StringVar()
def get_data():
    global yt,res,title,video_url,url,resolutions
    video_url = url.get() 
    yt = YouTube(video_url)
    title = yt.title

    #Download Thumbnail
    v_id = video_url.split('=')[1]+'.jpg'
    thumbnail_file = os.path.join(PATH,v_id)
    thumbnail = requests.get(yt.thumbnail_url)
    with open(thumbnail_file,'wb') as file:
        file.write(thumbnail.content)

    #Display Thumbnail
    img = Image.open(thumbnail_file)
    size = 300, 300
    img.thumbnail(size, Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img) 
    thumbnail_label = Label(window, image = img,bd = 5,relief = 'solid')
    thumbnail_label.grid(row=3,column=0,columnspan=2)
    thumbnail_label.image=img

    #Display Title of Video in Window
    title_message = Message(window, text=title, font=("Arial Bold",10),width=300,bd=10).grid(row=4,columnspan=2)
    available_res = [stream.resolution for stream in yt.streams.filter(progressive=True,file_extension='mp4').order_by("resolution")]
    
    #Select Avaialable Resolution of Video to Download
    choose_res = Label(window,text='Select Resolution').grid(row=5,column=0)
    resolutions = ttk.Combobox(window)
    resolutions['values'] = available_res
    resolutions.current(0)
    resolutions.grid(row = 5,column = 1)
    res = resolutions.get()
    #print(f"resolution = {res} title = {title}") 
    
    #Display Download Button
    download_btn = Button(window,text="Download Video",bd=5, relief='ridge', bg = 'violet', fg='Black', command = download).grid(row = 6, column = 0,columnspan = 2,pady = 3)

def download():
    download_label = Label(window,text = 'Downloading...',bd = 5).grid(row = 6,column = 0, columnspan=2,pady = 3)
    global yt,res,title,resolutions
    res = resolutions.get()
    #print(res)

    #Download Video in mp4 Format and Selected Resolution
    video = yt.streams.filter(file_extension = 'mp4',progressive = True,res = res)[0]
    video.download()
    
    #Display Video Downlaoded Messaged along with Path
    download_label = Label(window,text = 'Download Finished',bd = 5).grid(row = 6,column = 0, columnspan = 2,ipady = 3)
    success_message = Text(window,height = 5,width = 50,wrap = CHAR, bd = 0)
    success_message.insert(1.0,f'Video Downloaded \n {os.path.join(PATH,title)}')
    success_message.grid(row = 7, column = 0,columnspan = 2)
    success_message.configure(state =  "disabled")

L1 = Label(window,text='Enter Youtube Video URL', font = ('Arial',15)).grid(row = 0,column = 0, columnspan = 2)
url_Entry = Entry(window,textvariable = url, width = 60,bd = 10,relief = 'ridge').grid(row = 1, column = 0, pady = 5, ipady = 5,columnspan = 2)
find_video  =  Button(window,text = 'Find Video',bd = 5, relief = 'ridge',command = get_data).grid(row = 2, column = 0, columnspan = 2)
quit = Button(window, text = 'Close',bd = 5, relief = 'ridge',command = window.destroy).grid(row = 8, column = 0, columnspan = 2,rowspan = 2)
info = Label(window, text = 'Made by Aashutosh', font = ("Courier New",10)).grid(row = 15, column = 0, columnspan = 2)
window.mainloop()