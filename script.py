#FORMS
import tkinter as tk
from tkinter import ttk,messagebox
from tkinter import filedialog as fd 
from tkinter.constants import SUNKEN 
from tkinter.messagebox import showinfo
from numpy import ceil, log2 
import pandas as pd
import numpy as np 
from numpy import* 
import matplotlib.pyplot as plt 
from scipy.signal import butter, lfilter 
from scipy.fft import fft,fftfreq  
import math

#VARIABILI GLOBALI:
sf=0
sd=0
hf=0
lf=0
pf=0
filename=''
class window_Tk():
    #CLASS VARIABLES:
    y_temp=[]
    y=[]
    ordinata_x=[]

    def __init__(self,window):
        self.window=window

    def windowCostruction(self):
        self.window.attributes('-fullscreen',True)
        self.window.title('ANALYSIS')
        self.window.resizable(False, False)
        self.window.configure(bg='#f2bac7')

    def LabelCostruction(self,title,Xl,Yl,colour,arg,Xt,Yt):
        label = tk.Label(text=title)
        label.place(x=Xl,y=Yl)
        label.configure(bg=colour)
        global sf,dc,sd,hf,lf,pf
        if arg=='sf':
            sf=tk.Entry(width=60)
            sf.grid()
            sf.place(x=Xt,y=Yt)
        elif arg=='dc':
            dc=tk.Entry(width=60)
            dc.grid()
            dc.place(x=Xt,y=Yt)
        elif arg=='sd':
            sd=tk.Entry(width=60)
            sd.grid()
            sd.place(x=Xt,y=Yt)
        elif arg=='hf':
            hf=tk.Entry(width=60)
            hf.grid()
            hf.place(x=Xt,y=Yt)
        elif arg=='lf':
            lf=tk.Entry(width=60)
            lf.grid()
            lf.place(x=Xt,y=Yt)
        elif arg=='pf':
            pf = ttk.Combobox(window, 
                            values=["NO FILTERS","LOW PASS","HIGH PASS","BAND PASS"])
            pf.current(0)
            pf.place(x=Xt,y=Yt)

    def BottonCostruction(self,title,border,text_colour,bg_colour,function,Xb,Yb):
        if function=='select_file':
            bottone = tk.Button(self.window, text =title, relief=border,fg=text_colour,bg=bg_colour,command=self.select_file)
        elif function=='close':
            bottone = tk.Button(self.window, text =title, relief=border,fg=text_colour,bg=bg_colour,command=self.close)
        elif function=='verify':
            bottone = tk.Button(self.window, text =title, relief=border,fg=text_colour,bg=bg_colour,command=self.verify)
        elif function=='filteredGraph':
            bottone = tk.Button(self.window, text =title, relief=border,fg=text_colour,bg=bg_colour,command=self.filteredGraph)
        elif function=='spectrumGraph':
            bottone = tk.Button(self.window, text =title, relief=border,fg=text_colour,bg=bg_colour,command=self.spectrumGraph)
        
        bottone.place(x=Xb,y=Yb)
        
    def select_file(self):
        filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
        )
        global filename
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
    
        
    def close(self):
        window.destroy()

    def filteredGraph(self):
        x = np.arange(0,len(self.y_temp)/800,1/800)
        T = 1/int(sf.get())
        n = int(T * int(sf.get())) 
        if len(self.__class__.y)==len(self.__class__.ordinata_x):
            if pf.get()=='LOW PASS':
                self.__class__.y = self.butter_lowpass_filter(self.y_temp, float(lf.get()),int(sf.get()))
            elif pf.get()=='HIGH PASS':
                self.__class__.y = self.butter_highpass_filter(self.y_temp,float(lf.get()),int(sf.get()))
            elif pf.get()=='BAND PASS':
                self.__class__.y=self.butter_bandpass_filter(self.__class__.y_temp,float(hf.get()),float(lf.get()),int(sf.get())) 
            elif pf.get()=='NO FILTERS':
                self.__class__.y=self.__class__.y_temp
            
            plt.plot(x, self.y_temp, 'b-', label='data')
            plt.plot(x, self.__class__.y, 'g-', linewidth=2, label='filtered data')
            plt.xlabel('Time [sec]')
            plt.grid()
            plt.legend()
            plt.show()

    def spectrumGraph(self):
        T = 1.0 / int(sf.get())

        #graph of the spectrum without filters
        N = len(self.__class__.y_temp)
        media=mean(self.__class__.y_temp)
        ordinata_y_filtrata_media=self.__class__.y_temp-media
        n=log2(len(ordinata_y_filtrata_media))
        n=math.ceil(n)
        ordinata_y_filtrata_media = np.append(ordinata_y_filtrata_media, np.repeat(0,(pow(2,n))-N))
        yf = fft( ordinata_y_filtrata_media)
        N = pow(2, n)
        xf = fftfreq(N, T)[:N//2]
        plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
        
        #graph of the spectrum with filters
        N = len(self.__class__.y) 
        media=mean(self.__class__.y)
        ordinata_y_filtrata_media=self.__class__.y-media
        n=log2(len(ordinata_y_filtrata_media))
        n=math.ceil(n)
        ordinata_y_filtrata_media = np.append(ordinata_y_filtrata_media, np.repeat(0,(pow(2,n))-N))
        yf = fft( ordinata_y_filtrata_media)
        N = pow(2, n)
        xf = fftfreq(N, T)[:N//2]
        plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
        
        plt.show()


    def butter_lowpass(self,cutoff, fs, order=3):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a
    def butter_lowpass_filter(self,data, cutoff, fs, order=3):
        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def butter_highpass(self,cutoff, fs, order=3):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a
    def butter_highpass_filter(self,data, cutoff, fs, order=3):
        b, a = self.butter_highpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def butter_bandpass(self, highcut, lowcut, fs, order=3):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [high,low ], btype='band', analog=False)
        return b, a
    def butter_bandpass_filter(self,data, highcut, lowcut,  fs, order=3):
        b, a = self.butter_bandpass(highcut, lowcut,  fs, order=order)
        y = lfilter(b, a, data)
        return y

    def verify(self):
        cont=0
        lista_testi=[ ]
        lista_testi.append(dc.get())
        lista_testi.append(sf.get())
        lista_testi.append(sd.get())
        lista_testi.append(hf.get())
        lista_testi.append(lf.get())
        for i in lista_testi:
            cont+=1
            if len(i)==0:
                messagebox.showinfo(f'ATTENZIONE','NON HAI INSERITO TUTTI I DATI ')
                break
        if cont==len(lista_testi):
            messagebox.showinfo(f'BRAVO','DATI CARICATI!')
        y_temp = pd.read_csv(filename,  skiprows = 1, sep = ',',  header=None)
        self.__class__.y_temp=y_temp[int(dc.get())]
        self.__class__.ordinata_x=np.arange(0,(len(self.__class__.y))/int(sf.get()),1/int(sf.get()))
    
if __name__=='__main__':
    window=tk.Tk()
    dialog_window=window_Tk(window)
    dialog_window.windowCostruction()
    dialog_window.LabelCostruction('DATA COLUMN',100,170,'#f2bac7','dc',100,200)
    dialog_window.LabelCostruction('SKIP DATA',100,270,'#f2bac7','sd',100,300)
    dialog_window.LabelCostruction('POSSIBILE FILTERS',100,370,'#f2bac7','pf',100,400)
    dialog_window.LabelCostruction('HIGH FILTER',100,470,'#f2bac7','hf',100,500)
    dialog_window.LabelCostruction('LOW FILTER',100,570,'#f2bac7','lf',100,600)
    dialog_window.LabelCostruction('SAMPLE FREQUENCY',100,670,'#f2bac7','sf',100,700)
    
    dialog_window.BottonCostruction('UPLOAD FILE FROM BROWSE',SUNKEN,'white','#f71d86','select_file',100,100)
    dialog_window.BottonCostruction('CLOSE',SUNKEN,'white','#f71d86','close',1250,700)
    dialog_window.BottonCostruction('LOADING DATA',SUNKEN,'white','#f71d86','verify',750,700)
    dialog_window.BottonCostruction('GRAPH WITH FILTERED SIGNAL',SUNKEN,'white','#f71d86','filteredGraph',1050,700)
    dialog_window.BottonCostruction('SPECTRUM GRAPH',SUNKEN,'white','#f71d86','spectrumGraph',890,700)

    
    window.mainloop()