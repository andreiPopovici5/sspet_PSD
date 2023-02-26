from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
import sspet
import os
import pathlib
import tkinter.font as tkFont
from scipy.io.wavfile import read

######################CLOSE-GUI-FUNCTION###############
def close_gui():
    gui.destroy()
######################CLEAR-FRAMES FUNCTIONS###############
def clear_frameSignal():
    for widgets in frame_graph0.winfo_children():
      widgets.destroy()
    for widgets in frame_graph1.winfo_children():
      widgets.destroy()
    plot_graphsSignal()

def clear_frameAudio():
    for widgets in frameAudioGraph1.winfo_children():
      widgets.destroy()
    for widgets in frameAudioGraph2.winfo_children():
      widgets.destroy()
    plot_GraphsAudio()
    
######################PLOT-SIGNAL-GRAPH###############
def plot_graphsSignal():
    time,wave,freq,PowSpectDen=sspet.calculatePSDSignal(int(amp_entry_1.get()),int(freq_entry_1.get()),
                                                    int(amp_entry_2.get()),int(freq_entry_2.get()),
                                                    int(amp_entry_3.get()),int(freq_entry_3.get()),
                                                    int(amp_entry_4.get()),int(freq_entry_4.get()),
                                                    int(amp_entry_5.get()),int(freq_entry_5.get()),
                                                    int(amp_entry_6.get()),int(freq_entry_6.get()),
                                                    noise_slider.get())
    
    fig1 = Figure(figsize=(5, 4), dpi=100)
    ax = fig1.add_subplot()
    ax.plot(time,wave)
    ax.set_xlim([0,0.5])
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude [V]")

    canvas = FigureCanvasTkAgg(fig1, master=frame_graph0)
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, frame_graph0, pack_toolbar=False)
    toolbar.update()
    toolbar.pack(side=BOTTOM, fill=X)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    fig2 = Figure(figsize=(5, 4), dpi=100)
    bx = fig2.add_subplot()
    bx.semilogy(freq,PowSpectDen)
    bx.set_xlim([0,300])
    bx.set_xlabel('Frequency [Hz]')
    bx.set_ylabel('PSD [W/Hz]')

    canvas = FigureCanvasTkAgg(fig2, master=frame_graph1)
    canvas.draw()

    toolbar = NavigationToolbar2Tk(canvas, frame_graph1, pack_toolbar=False)
    toolbar.update()
    toolbar.pack(side=BOTTOM, fill=X)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

def plot_GraphsAudio():
  #import wav file w/ path
  file_name = os.path.join(os.path.dirname(__file__), 'audio')
  file_name = os.path.join(file_name, option.get())
  assert os.path.exists(file_name)

  #read file
  sampling_f_rec, rec=read(file_name)
  rec=rec.flatten()

  #calculate PSD of audio
  audio_f, audio_pow = sspet.calculatePSDAudio(sampling_f_rec,rec)
  
  #calculate audio time
  duration = len(rec)/sampling_f_rec
  time = np.arange(0,duration,1/sampling_f_rec)

  fig1 = Figure(figsize=(5, 4), dpi=100)
  ax = fig1.add_subplot()
  ax.plot(time,rec)
  ax.set_xlabel("Time [s]")
  ax.set_ylabel("Amplitude")

  canvas = FigureCanvasTkAgg(fig1, master=frameAudioGraph1)
  canvas.draw()
  toolbar = NavigationToolbar2Tk(canvas, frameAudioGraph1, pack_toolbar=False)
  toolbar.update()
  toolbar.pack(side=BOTTOM, fill=X)
  canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

  fig2 = Figure(figsize=(5, 4), dpi=100)
  bx = fig2.add_subplot()
  bx.semilogy(audio_f,audio_pow)
  bx.set_xlabel('Frequency [Hz]')
  bx.set_ylabel('PSD [W/Hz]')

  canvas = FigureCanvasTkAgg(fig2, master=frameAudioGraph2)
  canvas.draw()

  toolbar = NavigationToolbar2Tk(canvas, frameAudioGraph2, pack_toolbar=False)
  toolbar.update()
  toolbar.pack(side=BOTTOM, fill=X)
  canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)



######################MAIN-FUNCTION###############
#----------------WINDOW-SETTINGS-----------------
gui =Tk()
gui.title('Power Spectral Density')
window_width = 1200
window_height =600
screen_width = gui.winfo_screenwidth()
screen_height = gui.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
gui.geometry('{}x{}+{}+{}'.format(window_width, window_height, center_x, center_y))
gui.state('zoomed') 
gui.protocol('WM_DELETE_WINDOW', close_gui)

#----------------CREATE-TABS---------------------
customed_style = ttk.Style()
customed_style.configure('Custom.TNotebook.Tab', padding=[12, 12], font=('Helvetica', 10))

notebook = ttk.Notebook(gui,style='Custom.TNotebook')
notebook.pack(fill=BOTH,expand=True)

frameTab1 = ttk.Frame(notebook)
frameTab2 = ttk.Frame(notebook)
frameTab1.pack(fill=BOTH, expand=True)
frameTab2.pack(fill=BOTH, expand=True)
notebook.add(frameTab1, text='Signal')
notebook.add(frameTab2, text='Audio')


#----------------SIGNAL-TAB-SETUP--------------
frameTab1.rowconfigure(0, weight=1,uniform='half')
frameTab1.rowconfigure(1, weight=1,uniform='half')
frameTab1.columnconfigure(1, weight=1)
frameTab1.columnconfigure(0, weight=1)

#---------------SINGAL-TAB-CONTROL-SECTION--------
frame0=Frame(frameTab1)
frame0.grid(row=0,column=0, columnspan=2,sticky=NSEW)

frame0.columnconfigure(0, weight=1)
frame0.columnconfigure(1, weight=1)
frame0.columnconfigure(2, weight=1)
frame0.rowconfigure(0, weight=1)
frame0.rowconfigure(1, weight=1)
frame0.rowconfigure(2, weight=1)

#AMP-FRQ-1---------------
frame_control1=Frame(frame0)
frame_control1.columnconfigure(0, weight=1)
frame_control1.columnconfigure(1, weight=1)
amp_label_1=Label(frame_control1, text="Amplitude 1:").grid(row=0,column=0,sticky=E)
amp_entry_1=Entry(frame_control1)
amp_entry_1.insert(0, 5)
amp_entry_1.grid(row=0,column=1,padx=10,pady=10,sticky=W)
freq_label_1=Label(frame_control1, text="Frequency 1:").grid(row=1,column=0,sticky=E)
freq_entry_1=Entry(frame_control1)
freq_entry_1.insert(0, 10)
freq_entry_1.grid(row=1,column=1,padx=10,pady=10,sticky=W)
frame_control1.grid(column=0, row=0, sticky="N"+"E"+"W")

#AMP-FRQ-2---------------
frame_control2=Frame(frame0)
frame_control2.columnconfigure(0, weight=1)
frame_control2.columnconfigure(1, weight=1)
amp_label_2=Label(frame_control2, text="Amplitude 2:").grid(row=0,column=0,sticky=E)
amp_entry_2=Entry(frame_control2)
amp_entry_2.insert(0, 0)
amp_entry_2.grid(row=0,column=1,padx=10,pady=10,sticky=W)
freq_label_2=Label(frame_control2, text="Frequency 2:").grid(row=1,column=0,sticky=E)
freq_entry_2=Entry(frame_control2)
freq_entry_2.insert(0, 0)
freq_entry_2.grid(row=1,column=1,padx=10,pady=10,sticky=W)
frame_control2.grid(column=1, row=0,sticky="N"+"E"+"W")

#AMP-FRQ-3---------------
frame_control3=Frame(frame0)
frame_control3.columnconfigure(0, weight=1)
frame_control3.columnconfigure(1, weight=1)
amp_label_3=Label(frame_control3, text="Amplitude 3:").grid(row=0,column=0,sticky=E)
amp_entry_3=Entry(frame_control3)
amp_entry_3.insert(0, 0)
amp_entry_3.grid(row=0,column=1,padx=10,pady=10,sticky=W)
freq_label_3=Label(frame_control3, text="Frequency 3:").grid(row=1,column=0,sticky=E)
freq_entry_3=Entry(frame_control3)
freq_entry_3.insert(0, 0)
freq_entry_3.grid(row=1,column=1,padx=10,pady=10,sticky=W)
frame_control3.grid(column=2, row=0,sticky="N"+"E"+"W")

#AMP-FRQ-4---------------
frame_control4=Frame(frame0)
frame_control4.columnconfigure(0, weight=1)
frame_control4.columnconfigure(1, weight=1)
amp_label_4=Label(frame_control4, text="Amplitude 4:").grid(row=0,column=0,sticky=E)
amp_entry_4=Entry(frame_control4)
amp_entry_4.insert(0, 0)
amp_entry_4.grid(row=0,column=1,padx=10,pady=10,sticky=W)
freq_label_4=Label(frame_control4, text="Frequency 4:").grid(row=1,column=0,sticky=E)
freq_entry_4=Entry(frame_control4)
freq_entry_4.insert(0, 0)
freq_entry_4.grid(row=1,column=1,padx=10,pady=10,sticky=W)
frame_control4.grid(column=0, row=1, sticky="N"+"E"+"W")

#AMP-FRQ-5---------------
frame_control5=Frame(frame0)
frame_control5.columnconfigure(0, weight=1)
frame_control5.columnconfigure(1, weight=1)
amp_label_5=Label(frame_control5, text="Amplitude 5:").grid(row=0,column=0,sticky=E)
amp_entry_5=Entry(frame_control5)
amp_entry_5.insert(0, 0)
amp_entry_5.grid(row=0,column=1,padx=10,pady=10,sticky=W)
freq_label_5=Label(frame_control5, text="Frequency 5:").grid(row=1,column=0,sticky=E)
freq_entry_5=Entry(frame_control5)
freq_entry_5.insert(0, 0)
freq_entry_5.grid(row=1,column=1,padx=10,pady=10,sticky=W)
frame_control5.grid(column=1, row=1, sticky="N"+"E"+"W")

#AMP-FRQ-6---------------
frame_control6=Frame(frame0)
frame_control6.columnconfigure(0, weight=1)
frame_control6.columnconfigure(1, weight=1)
amp_label_6=Label(frame_control6, text="Amplitude 6:").grid(row=0,column=0,sticky=E)
amp_entry_6=Entry(frame_control6)
amp_entry_6.insert(0, 0)
amp_entry_6.grid(row=0,column=1,padx=10,pady=10,sticky=W)
freq_label_6=Label(frame_control6, text="Frequency 6:").grid(row=1,column=0,sticky=E)
freq_entry_6=Entry(frame_control6)
freq_entry_6.insert(0, 0)
freq_entry_6.grid(row=1,column=1,padx=10,pady=10,sticky=W)
frame_control6.grid(column=2, row=1,sticky="N"+"E"+"W")

#NOISE-SLIDER---------------
frame_control7=Frame(frame0)
noise_label=Label(frame_control7, text="Noise",font=(16)).pack()
noise_slider=Scale(frame_control7,from_=0, to=50,orient=HORIZONTAL)
noise_slider.set(2)
noise_slider.pack(padx=120,pady=10,expand=TRUE, fill=BOTH)
frame_control7.grid(column=0, row=2, columnspan=2, sticky=NSEW)

#REFRESH-BUTTON---------------
frame_control8=Frame(frame0)
refresh_Button = Button(frame_control8, text ="Refresh", bg="dark gray", command = clear_frameSignal, font=tkFont.Font(size=16))
refresh_Button.pack(padx=50,pady=40,expand=TRUE, fill=BOTH)
frame_control8.grid(column=2, row=2, sticky=NSEW)

#---------------SINGAL-TAB-GRAPH-SECTION--------
frame1=Frame(frameTab1)
frame1.grid(row=1,column=0, columnspan=2,sticky=NSEW)
frame1.rowconfigure(1, weight=1,uniform="half2")
frame1.rowconfigure(0, weight=1,uniform="half2")
frame1.columnconfigure(0, weight=1)
frame1.columnconfigure(1, weight=1)
frame_graph0=Frame(frame1)
frame_graph0.grid(row=0,column=0,rowspan=2,sticky=NSEW)
frame_graph1=Frame(frame1)
frame_graph1.grid(row=0,column=1,rowspan=2,sticky=NSEW)


#----------------AUDIO-TAB-SETUP--------------
frameTab2.rowconfigure(0, weight=1,uniform='half3')
frameTab2.rowconfigure(1, weight=2,uniform='half3')
frameTab2.rowconfigure(2, weight=2,uniform='half3')
frameTab2.columnconfigure(1, weight=1)
frameTab2.columnconfigure(0, weight=1)


frameAudio=Frame(frameTab2)
frameAudio.rowconfigure(1, weight=1)
frameAudio.rowconfigure(0, weight=1)
frameAudio.columnconfigure(0, weight=1,uniform="half4")
frameAudio.columnconfigure(1, weight=1,uniform="half4")
#get file path
filePath=pathlib.Path(__file__).parent.resolve()
#join audio folder path 
audioPath=os.path.join(filePath, "audio")
audioFiles=dir_list = os.listdir(audioPath)

#----------------AUDIO-COLTROL-SECTION--------------
option=StringVar()
option.set(audioFiles[0])
dropMenu=OptionMenu(frameAudio, option, *audioFiles)
dropMenu.config(font=tkFont.Font(size=16), bg='dark gray')

menu = frameAudio.nametowidget(dropMenu.menuname)
menu.config(font=tkFont.Font(size=16), bg='dark gray')

dropMenu.grid(row=0,column=0,rowspan=2,sticky=NSEW, padx=160, pady=40)
refreshAduio = Button(frameAudio, text ="Refresh", bg="dark gray", command= clear_frameAudio,font=tkFont.Font(size=16))
refreshAduio.grid(row=0,column=1,rowspan=2,sticky=NSEW, padx=160, pady=40)
frameAudio.grid(row=0,column=0,columnspan=2,sticky=NSEW)

#----------------AUDIO-GRAPH-SECTION--------------
frameAudioGraph1=Frame(frameTab2)
frameAudioGraph1.grid(row=1,column=0,columnspan=2,sticky=NSEW)
frameAudioGraph2=Frame(frameTab2, background="green")
frameAudioGraph2.grid(row=2,column=0,columnspan=2,sticky=NSEW)

plot_graphsSignal()
plot_GraphsAudio()
gui.mainloop()

