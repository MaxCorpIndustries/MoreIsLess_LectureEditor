import tkinter as tk
from tkinter import ttk
import math
import sys
import subprocess
import os
import shutil
from moviepy.editor import AudioClip, VideoFileClip, concatenate_videoclips
from moviepy.audio.fx.volumex import volumex
import time
import multiprocessing
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.messagebox import showinfo
import threading
from proglog import ProgressBarLogger

root = tk.Tk()
'''

       __   __   ___       __           ___  __   __          
 |\/| /  \ |__) |__     | /__`    |    |__  /__` /__` 
 |  | \__/ |  \ |___    | .__/    |___ |___ .__/ .__/          
                                                               
      ___  __  ___       __   ___     ___  __    ___  __   __  
|    |__  /  `  |  |  | |__) |__     |__  |  \ |  |  /  \ |__) 
|___ |___ \__,  |  \__/ |  \ |___    |___ |__/ |  |  \__/ |  \ 
                                                               
made by: Maximo Perasso

This software was meant to make the lecture videos from professors
a lot easier to learn from if the instructor likes to wait or perhaps talks
a bit too slow or too fast.
'''
notice1 = '''
No malice is intended, this software is purely
to enhance the content from the instructor
for students who prefer different learning styles.
'''
notice2 = '''
This software is not magic, it cannot help if you
simply do not understand the content.
Asking a teacher for help is always the best way to
understand the topic.
'''

#application title
normalTitle="'More Is Less' Lecture Editor"
secretTitle="'Moore Is Less' Lecture Editor"
root.title(normalTitle)
lastUpdate = "1/13/2022"
VersionNum="1.5.0"

#colors
PanelsBackgroundColor = '#444444'
CanvasBackgroundColor = '#2A2A50'
TitleColor1 = "#5EBD3E"
TitleColor2 = '#FFB900'
TitleColor3 = '#F78200'
TitleColor4 = '#E23838'
TitleColor5 = '#973999'
TitleColor6 = '#009CDF'
TitleInfoColor = '#D58F08'
TextColor = "#FFFFFF"

textfont=('Terminal', 15)

#quality settings

Preset_list = ['ultrafast','superfast','veryfast','faster','fast','medium','slow','slower','veryslow','placebo']
Codec_list=['libx264','mpeg4','rawvideo','png','libvorbis','libvpx']
codec_help=["'libx264' (default codec for file extension .mp4) makes well-compressed videos (quality tunable using ‘bitrate’).","'mpeg4' (other codec for extension .mp4) can be an alternative to 'libx264', and produces higher quality videos by default.","'rawvideo' (use file extension .avi) will produce a video of perfect quality, of possibly very huge size.","png (use file extension .avi) will produce a video of perfect quality, of smaller size than with rawvideo.","'libvorbis' (use file extension .ogv) is a nice video format, which is completely free/ open source. However not everyone has the codecs installed by default on their machine.","'libvpx' (use file extension .webm) is tiny a video format well indicated for web videos (with HTML5). Open source."]


#basic screen params
ScreenWidth = 800
ScreenHeight = 600
root.geometry(str(ScreenWidth)+"x"+str(ScreenHeight))
root.resizable(False, False)
root.configure(bg=PanelsBackgroundColor)

#frame declarations
frame = tk.Frame(root,bg=PanelsBackgroundColor)
frame.pack()

topframe = tk.Frame(root,bg=PanelsBackgroundColor)
topframe.pack(side = 'top' )

leftframe = tk.Frame(root,bg=PanelsBackgroundColor)
leftframe.pack(side = 'left' )

rightframe = tk.Frame(root,bg=PanelsBackgroundColor)
rightframe.pack(side = 'right' )

bottomframe = tk.Frame(root,bg=PanelsBackgroundColor)
bottomframe.pack(side = 'bottom' )

#spacer vars for drop down selectors
Spacer_gen_x = 50

Selectable_gen_x = 25
Spacer_button_margin_y = 50

#creating empty preset arrays to fill in w/ file
PRESETS     = []
PRESET_VOL  = []
PRESET_SPD  = []
PRESET_LVL  = []
RES         = []


codec=Codec_list[0]
preset = Preset_list[0]
cut_out_window=0.1
ease_between_cut=0.0

audio_codec="aac"


#get data from instructor file
instructor_file = "instructor.txt"
resolution_file = "resolutions.txt"

file = open(instructor_file,'r')
file_text = file.read()
for x in file_text.splitlines():
    data = x.split(',')
    PRESETS.append(data[0])
    PRESET_VOL.append(int(data[1]))
    PRESET_SPD.append(float(data[2]))
    PRESET_LVL.append(float(data[3]))
file.close()

#get data from resolution file
file = open(resolution_file,'r')
RES = file.read().splitlines()
file.close()

ThreadCount = multiprocessing.cpu_count() #get CPU thread count
file_in = ""  # Input file path
quietPointCounter=0 #define var for counting quiet points.
file_out = "" # Output file path

#creating the title and update day splash at the top
#---------------------------------
canvasHeight=40

#create the canvas
canvas=tk.Canvas(topframe,
                 relief='groove',
                 bd=0,
                 width=ScreenWidth,
                 height=canvasHeight,
                 bg=CanvasBackgroundColor)

#create the title text and update text
titlefont=('Terminal', 18)
titlePosX = 3.25
titleText = normalTitle
titlelayer1=canvas.create_text((ScreenWidth/titlePosX),(canvasHeight/1.8),text=titleText,fill=TitleColor5,font=titlefont)
titlelayer2=canvas.create_text((ScreenWidth/titlePosX),(canvasHeight/2),text=titleText,fill=TitleColor4,font=titlefont)
titlelayer3=canvas.create_text((ScreenWidth/titlePosX),(canvasHeight/2.2),text=titleText,fill=TitleColor3,font=titlefont)
titlelayer4=canvas.create_text((ScreenWidth/titlePosX),(canvasHeight/2.3),text=titleText,fill=TitleColor2,font=titlefont)
titlelayer5=canvas.create_text((ScreenWidth/titlePosX),(canvasHeight/2.5),text=titleText,fill=TitleColor1,font=titlefont)
titlelayer6=canvas.create_text((ScreenWidth/1.25),(canvasHeight/2),text='Created by: {REDACTED}\n Version: '+ VersionNum +' , Last update: '+lastUpdate,fill=TitleInfoColor,font=('System', 10) )

#pack the canvas to the UI
canvas.pack(fill='x')
#END

##-------------------##
## Presets/Settings: ##
##-------------------##

infoTextPrompt="Info & Status:\nCPU threads detected:      {0}\nQuiet points:              {1}\nProcessing ETA:       {2}\n\nInput Video Filename:\n{3}\n\nOutput Video Filename:\n{4}\n\nStatus and progress:\n{5}\n\nExport Progress: \n{6}/3 steps"
infoTextFormatted=infoTextPrompt.format(ThreadCount,quietPointCounter,0,file_in,file_out,0,0)
def updatePresets(instructor,*args):
    '''
    This function gets the current preset from the preset dropdown and
    refrences the 3 relevant 'preset' arrays (grabbed from instructor file)
    to load the presets for that instructor.
    '''
    for i in PRESETS:                               #go through list of presets
        if(Preset_Dropdown_Selection.get() == i):   #check which preset was found

            f = PRESETS.index(i)                    #find array index of that preset
            
            #use index num to set presets from equally sized arrays
            Volume_Slider.set(int(PRESET_VOL[f]))
            Level_Slider.set(float(PRESET_LVL[f]))
            Speed_Slider.set(float(PRESET_SPD[f]))
            break                           #prevent system from going to next preset

def open_popup():
   top= tk.Toplevel(root,bg='black')
   top.geometry("500x350")
   top.title("Complaints and Info , Startup Popup")
   
   tk.Label(top, text= "NOTICE TO PROFESSORS WHO SEE THIS:", font=('Consolas',16),fg='red',anchor="w",bg='black').pack(side='top')
   tk.Label(top, text= notice1, font=('Arial'),anchor="w",bg='black',fg='white').pack(side='top')
   tk.Label(top, text= "NOTICE TO STUDENTS WHO USE THIS:", font=('Consolas',16),fg='red',anchor="w",bg='black').pack(side='top')
   tk.Label(top, text= notice2, font=('Arial'),anchor="w",bg='black',fg='white').pack(side='top')

   tk.Label(top, text= "direct any and all complaints to this email: \nMoreIsLessSoftware@gmail.com", font=('Arial'),anchor="w",bg='black',fg='yellow').pack(side='bottom',pady=10)
   
   root.lift()
   top.resizable(False, False)

def meme():
    '''
    this function controls
    updating the title name
    '''
    
    canvas.itemconfigure(titlelayer1, text=secretTitle)
    canvas.itemconfigure(titlelayer2, text=secretTitle)
    canvas.itemconfigure(titlelayer3, text=secretTitle)
    canvas.itemconfigure(titlelayer4, text=secretTitle)
    canvas.itemconfigure(titlelayer5, text=secretTitle)

def file_save():
    global file_out
    files = [('Video File', '*.mp4')]
    fileOutput = fd.asksaveasfile(filetypes = files, defaultextension = files)
    file_out=fileOutput.name
    InfoBox.config(text = infoTextPrompt.format(ThreadCount,quietPointCounter,0,file_in,file_out,0,0))
      
def select_file():
    global file_in
    filetypes = (
        ('mp4', '*.mp4'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message="File loaded: \n" + filename
    )
    file_in = filename
    InfoBox.config(text = infoTextPrompt.format(ThreadCount,quietPointCounter,0,file_in,file_out,0,0))

    
#from https://gist.github.com/vivekhaldar/595af6c6aa06ed061f6f3f6c97d087c3
    
#def find_speaking(audio_clip, window_size, volume_threshold, ease_in):
def find_speaking(audio_clip, window_size=0.1, volume_threshold=0.01, ease_in=0.00):

    global quietPointCounter
    # First, iterate over audio to find all silent windows.
    num_windows = math.floor(audio_clip.end/window_size)
    window_is_silent = []
    for i in range(num_windows):
        s = audio_clip.subclip(i * window_size, (i + 1) * window_size)
        v = s.max_volume()
        window_is_silent.append(v < volume_threshold)
        if(v < volume_threshold):
            quietPointCounter+=1

    # Find speaking intervals.
    speaking_start = 0
    speaking_end = 0
    speaking_intervals = []
    
    for i in range(1, len(window_is_silent)):
        e1 = window_is_silent[i - 1]
        e2 = window_is_silent[i]
        
        # silence -> speaking
        if e1 and not e2:
            speaking_start = i * window_size
        # speaking -> silence, now have a speaking interval
        if not e1 and e2:
            speaking_end = i * window_size
            new_speaking_interval = [speaking_start - ease_in, speaking_end + ease_in]
            # With tiny windows, this can sometimes overlap the previous window, so merge.
            need_to_merge = len(speaking_intervals) > 0 and speaking_intervals[-1][1] > new_speaking_interval[0]
            if need_to_merge:
                merged_interval = [speaking_intervals[-1][0], new_speaking_interval[1]]
                speaking_intervals[-1] = merged_interval
            else:
                speaking_intervals.append(new_speaking_interval)
    #print(speaking_intervals)
    return speaking_intervals

S00_bar = "░░░░░░░░░░░░░░░"
S10_bar = "█░░░░░░░░░░░░░░"
S25_bar = "████░░░░░░░░░░░"
S50_bar = "███████░░░░░░░░"
S80_bar = "███████████░░░░"
S90_bar = "█████████████░░"
SDN_bar = "███████████████"

class GUILogger(ProgressBarLogger):

    def callback(self, **changes):
        # Every time the logger is updated, this function is called with
        # the `changes` dictionnary of the form `parameter: new value`.
        
        for (parameter, new_value) in changes.items():
            print(changes)


def Test2(keep_clips):
    edited_video = concatenate_videoclips(keep_clips)
    time.sleep(2)
    InfoBox.config(text = infoTextPrompt.format(ThreadCount,quietPointCounter,str(quietPointCounter*0.75)+" min",file_in,file_out,S25_bar,0))

    edited_video = volumex(edited_video, int(Volume_Slider.get()/100)) # doubles audio volume
    time.sleep(2)
    InfoBox.config(text = infoTextPrompt.format(ThreadCount,quietPointCounter,str(quietPointCounter*0.75)+" min",file_in,file_out,S50_bar,0))    


    time.sleep(0.5)
    InfoBox.config(text = infoTextPrompt.format(ThreadCount,quietPointCounter,str(quietPointCounter*0.75)+" min",file_in,file_out,S80_bar,0))

    my_logger = GUILogger()
    
    edited_video.write_videofile(file_out,
        fps=int(Fps_Slider.get()),
        preset=preset,
        codec=codec,
        audio_codec=audio_codec,
        threads=ThreadCount,
        logger=my_logger,
        verbose=True
                            
    )
    InfoBox.config(text = infoTextPrompt.format(ThreadCount,quietPointCounter,str(quietPointCounter*0.75)+" min",file_in,file_out,S90_bar,0))
    time.sleep(0.1)

    InfoBox.config(text = infoTextPrompt.format(ThreadCount,quietPointCounter,str(quietPointCounter*0.75)+" min",file_in,file_out,SDN_bar,0))    
    

def Test():
    vid = VideoFileClip(file_in)
    
    intervals_to_keep = find_speaking(vid.audio)
     
    keep_clips = [vid.subclip(start, end) for [start, end] in intervals_to_keep]
    
    print(keep_clips)
    InfoBox.config(text = infoTextPrompt.format(ThreadCount,quietPointCounter,str(quietPointCounter*0.75)+" min",file_in,file_out,S10_bar,0))

    threading.Thread(target=Test2(keep_clips)).start()  


def BeginProcessing():

    
    #prevent the program from running without input/output files.
    if((file_in == "")or(file_out=="")or(file_in == file_out)):
        mb.showerror("Error","Please make sure both the lecture video \nand the output video are set (and are different files) before starting.")
        InfoBox.config(text = infoTextPrompt.format(ThreadCount,quietPointCounter,"ERROR",file_in,file_out,"NEED INPUT AND OUTPUT FILES",0))
        return
    print("run")
    InfoBox.config(text = infoTextPrompt.format(ThreadCount,quietPointCounter,"RUN",file_in,file_out,S00_bar,0))
    keep_clips = threading.Thread(target=Test).start()
    
#creating the preset dropdown text
#---------------------------------
Preset_Dropdown_Text = tk.Label(
    leftframe,
    text='professor presets:',
    font=textfont,
    fg=TextColor,
    bg=PanelsBackgroundColor
)

Preset_Dropdown_Text.pack(
    padx=Spacer_gen_x,
    pady=0,
    fill='x',
    side='top'
)
#END 


#creating the preset dropdown
#---------------------------------

Preset_Dropdown_Selection = tk.StringVar(leftframe) #create preset dropdown

Preset_Dropdown_Selection.set(PRESETS[0]) # default value

Preset_Dropdown_Selection.trace("w", callback = updatePresets) #call updatePresets if the user changes it

Preset_Dropdown = tk.OptionMenu(leftframe, Preset_Dropdown_Selection,*PRESETS)
Preset_Dropdown.pack(
    padx=Selectable_gen_x,
    pady=1,
    fill='x',
    side='top'
)
#END



#creating the resolution dropdown text
#---------------------------------
Res_Dropdown_Text = tk.Label(
    leftframe,
    text='resolution (larger=bigger file):',
    font=textfont,
    fg=TextColor,
    bg=PanelsBackgroundColor
)

Res_Dropdown_Text.pack(
    padx=Spacer_gen_x,
    pady=2,
    fill='x',
    side='top'
)
#END

#creating the resolution dropdown
#---------------------------------
Res_Dropdown_Selection = tk.StringVar(leftframe)
Res_Dropdown_Selection.set(RES[0]) # default value

Res_Dropdown = tk.OptionMenu(leftframe, Res_Dropdown_Selection,*RES)
Res_Dropdown.pack(
    padx=Selectable_gen_x,
    pady=0,
    fill='x',
    side='top'
)
#END


#creating the quality text
#---------------------------------
Quality_Dropdown_Text = tk.Label(
    leftframe,
    text='quality (faster=bigger file):',
    font=textfont,
    fg=TextColor,
    bg=PanelsBackgroundColor
)

Quality_Dropdown_Text.pack(
    padx=Spacer_gen_x,
    pady=2,
    fill='x',
    side='top'
)
#END

#creating the quality dropdown
#---------------------------------
Quality_Dropdown_Selection = tk.StringVar(leftframe)
Quality_Dropdown_Selection.set(Preset_list[0]) # default value

Quality_Dropdown = tk.OptionMenu(leftframe, Quality_Dropdown_Selection,*Preset_list)
Quality_Dropdown.pack(
    padx=Selectable_gen_x,
    pady=0,
    fill='x',
    side='top'
)
#END


#creating the codec text
#---------------------------------
Codec_Dropdown_Text = tk.Label(
    leftframe,
    text='Video Codec (advanced):',
    font=textfont,
    fg=TextColor,
    bg=PanelsBackgroundColor
)

Codec_Dropdown_Text.pack(
    padx=Spacer_gen_x,
    pady=2,
    fill='x',
    side='top'
)
#END

#creating the codec dropdown
#---------------------------------
Codec_Dropdown_Selection = tk.StringVar(leftframe)
Codec_Dropdown_Selection.set(Codec_list[0]) # default value

Quality_Dropdown = tk.OptionMenu(leftframe, Codec_Dropdown_Selection,*Codec_list)
Quality_Dropdown.pack(
    padx=Selectable_gen_x,
    pady=0,
    fill='x',
    side='top'
)
#END

#creating a spacer
#---------------------------------
Spacer2 = tk.Label(
    leftframe,
    bg=PanelsBackgroundColor
)

Spacer2.pack(
    padx=Spacer_gen_x,
    pady=5,
    fill='x',
    side='top'
)
#END

#creating the preview button
#---------------------------------
preview_Button = tk.Button(leftframe, text="PREVIEW LECTURE",bg='#0A854E', fg="white",font=textfont)
preview_Button.pack(
    padx=Selectable_gen_x,
    pady=0,
    fill='x',
    side='top'
)
#END

#creating the start button
#---------------------------------
start_Button = tk.Button(rightframe, text="PROCESS FULL LECTURE",bg='green', fg="white",font=textfont,command=BeginProcessing)
start_Button.pack(
    padx=10,
    pady=10,
    fill='x',
    side='bottom'
)
#END

#creating the file button
#---------------------------------
video_save_button = tk.Button(rightframe, text="SAVE output file",bg='#CB0D9E', fg="white",font=textfont,command=file_save)
video_save_button.pack(
    padx=10,
    pady=10,
    fill='x',
    side='bottom'
)
#END

#creating the file button
#---------------------------------
video_load_button = tk.Button(rightframe, text="LOAD Lecture Video",bg='#B4910D', fg="white",font=textfont,command=select_file)
video_load_button.pack(
    padx=10,
    pady=10,
    fill='x',
    side='bottom'
)
#END
    


#creating a spacer
#---------------------------------
InfoBox = tk.Label(
    leftframe,
    anchor='nw',
    bd =10,
    bg='#E4E4E4',
    relief='sunken',
    width=30,
    height=80,
    justify=tk.LEFT,
    wraplength=300,
    compound = tk.TOP,
    text=infoTextFormatted,
    font=("Lucida Console",11),
    fg='black',
    

)

InfoBox.pack(
    padx=10,
    pady=10,
    fill='x',
    side='bottom'
)
#END



##------------------##
## SLIDERS SECTION: ##
##------------------##

#creating a spacer
#---------------------------------
Spacer4 = tk.Label(
    rightframe,
    bg=PanelsBackgroundColor
)

Spacer4.pack(
    padx=0,
    pady=200,
    fill='y',
    side='left'
)
#END

#creating a spacer
#---------------------------------
Spacer5 = tk.Label(
    rightframe,
    bg=PanelsBackgroundColor
)

Spacer5.pack(
    padx=50,
    pady=15,
    fill='y',
    side='bottom'
)
#END


#creating the volume text
#---------------------------------
Res_Dropdown_Text = tk.Label(
    rightframe,
    text='\nFPS    Volume   Speed    cutoff',
    font=textfont,
    fg=TextColor,
    bg=PanelsBackgroundColor
)

Res_Dropdown_Text.pack(
    padx=5,
    pady=2,
    fill='x',
    side='top'
)
#END

#creating the fps slider
#---------------------------------
Fps_Slider = tk.Scale(rightframe,bd =0,font=TextColor,fg='white',
                        from_=144,
                        to=24,
                        orient=tk.VERTICAL,
                        resolution=1,
                        bg=PanelsBackgroundColor
                        )
Fps_Slider.set(60)
Fps_Slider.pack(
    padx=20,
    pady=0,
    fill='y',
    side='left'
)
#END

#creating the vol slider
#---------------------------------
Volume_Slider = tk.Scale(rightframe,bd =0,font=TextColor,fg='white',
                         from_=200,
                         to=0,
                         orient=tk.VERTICAL,
                         resolution=1,
                         bg=PanelsBackgroundColor)
Volume_Slider.set(100)            
Volume_Slider.pack(
    padx=20,
    pady=0,
    fill='y',
    side='left'
)
#END

#creating the speed slider
#---------------------------------
Speed_Slider = tk.Scale(rightframe,bd =0,font=TextColor,fg='white',
                        from_=3,
                        to=0,
                        orient=tk.VERTICAL,
                        resolution=0.1,
                        bg=PanelsBackgroundColor
                        )
Speed_Slider.set(1.0)
Speed_Slider.pack(
    padx=20,
    pady=0,
    fill='y',
    side='left'
)
#END

#creating the Audio Level slider
#---------------------------------
Level_Slider = tk.Scale(rightframe,bd =0,font=TextColor,fg='white',
                        from_=0.5,
                        to=0,
                        orient=tk.VERTICAL,
                        resolution=0.001,
                        bg=PanelsBackgroundColor
                        )
Level_Slider.set(0.25)
Level_Slider.pack(
    padx=20,
    pady=0,
    fill='y',
    side='left'
)
#END

open_popup()

root.mainloop()


