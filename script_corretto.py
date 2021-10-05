#moduli utili:
import tkinter as tk
from tkinter import ttk,messagebox
from tkinter import filedialog as fd 
from tkinter.constants import SUNKEN #per bordo label
from tkinter.messagebox import showinfo
from numpy import ceil, log2 #per finestre di dialogo
import pandas as pd #per grafico
#per grafico:
import numpy as np #per grafico
from numpy import* #per grafico
import matplotlib.pyplot as plt #per grafico 
from scipy.signal import butter, lfilter #per filtraggio
from scipy.fft import fft,fftfreq    #per fourier
import math
#VARIABILI GLOBALI:
sf=0
sd=0
hf=0
lf=0
pf=0
filename=''
class window_Tk():
    #VARIABILI DI CLASSE:
    file_da_analizzare=[]
    ordinata_y_temp=[]
    ordinata_y_filtrata=[]
    ordinata_x=[]

    def __init__(self,window):
        self.window=window

    def costruzione_finestra(self):
        self.window.attributes('-fullscreen',True)
        self.window.title('ANALYSIS')
        self.window.resizable(False, False)
        self.window.configure(bg='#f2bac7')

    def creazione_label(self,title,Xl,Yl,colour,arg,Xt,Yt):
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
                            values=["NO FILTERS","PASSA BASSO","PASSA ALTO","PASSA BANDA"])
            pf.current(0)
            pf.place(x=Xt,y=Yt)

    def creazione_bottoni(self,title,border,text_colour,bg_colour,function,Xb,Yb):
        
        if function=='select_file':
            bottone = tk.Button(self.window, text =title, relief=border,fg=text_colour,bg=bg_colour,command=self.select_file)
        elif function=='chiudi':
            bottone = tk.Button(self.window, text =title, relief=border,fg=text_colour,bg=bg_colour,command=self.chiudi)
        elif function=='verifica':
            bottone = tk.Button(self.window, text =title, relief=border,fg=text_colour,bg=bg_colour,command=self.verifica)
        elif function=='disegna_grafico_filtrato':
            bottone = tk.Button(self.window, text =title, relief=border,fg=text_colour,bg=bg_colour,command=self.disegna_grafico_filtrato)
        elif function=='disegna_grafico_spettro':
            bottone = tk.Button(self.window, text =title, relief=border,fg=text_colour,bg=bg_colour,command=self.disegna_grafico_spettro)
        
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
    
        
    def chiudi(self):
        window.destroy()

    def disegna_grafico_filtrato(self):
        if len(self.__class__.ordinata_y_filtrata)==len(self.__class__.ordinata_x):
            plt.plot(self.__class__.ordinata_x,self.__class__.ordinata_y_filtrata)
            plt.show()
        else:
            messagebox.showinfo('ATTENZIONE','ERRORE DURANTE LA CREAZIONE DEL GRAFICO, RICONTROLLARE I DATI')

    def disegna_grafico_spettro(self):
        N = len(self.__class__.ordinata_y_filtrata)  # Number of sample points
        # # sample spacing
        T = 1.0 / int(sf.get())

        media=mean(self.__class__.ordinata_y_filtrata)
        ordinata_y_filtrata_media=self.__class__.ordinata_y_filtrata-media

        n=log2(len(ordinata_y_filtrata_media))
       # n=math.floor(n)
        n=math.ceil(n)
        ordinata_y_filtrata_media = np.append(ordinata_y_filtrata_media, np.repeat(0,(pow(2,n))-N))
        yf = fft( ordinata_y_filtrata_media)

        N = pow(2, n)

        xf = fftfreq(N, T)[:N//2]
        plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
        plt.show()

    def butter_lowpass(self,cutOff, fs, order=5):
        nyq = 0.5 * fs
        normalCutoff = cutOff / nyq
        b, a = butter(order, normalCutoff, btype='low', analog = True)
        return b, a

    def butter_lowpass_filter(self,data, cutOff, fs, order=4):
        b, a = self.butter_lowpass(cutOff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def butter_highpass(self,cutOn, fs, order=5):
        nyq = 0.5 * fs
        normalCutOn = cutOn / nyq
        b, a = butter(order, normalCutOn, btype='low', analog = True)
        return b, a

    def butter_highpass_filter(self,data, cutOn, fs, order=4):
        b, a = self.butter_highpass(cutOn, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def butter_bandpass(self,cutOff,cutOn, fs, order=5):
        nyq = 0.5 * fs
        normalbandoff = (cutOn-cutOff) / nyq
        b, a = butter(order, normalbandoff, btype='low', analog = True)
        return b, a

    def butter_bandpass_filter(self,data, cutOff,cutOn, fs, order=4):
        b, a = self.butter_bandpass(cutOff,cutOn, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def filtraggio(self):
        if pf.get()=='PASSA BASSO':
            self.__class__.ordinata_y_filtrata=self.butter_lowpass_filter(self.__class__.ordinata_y_temp,int(lf.get()),int(sf.get()))
        elif pf.get()=='PASSA ALTO':
           self.__class__.ordinata_y_filtrata=self.butter_highpass_filter(self.__class__.ordinata_y_temp,int(hf.get()),int(sf.get()))    
        elif pf.get()=='PASSA BANDA':
           self.__class__.ordinata_y_filtrata=self.butter_bandpass_filter(self.__class__.ordinata_y_temp,int(lf.get()),int(hf.get()),int(sf.get())) 
        elif pf.get()=='NO FILTERS':
            self.__class__.ordinata_y_filtrata=self.__class__.ordinata_y_temp
            
    def verifica(self):
        cont=0 #contatore per andare avanti se si è inserito tutto correttamente
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
        #ORDINATE:
        y_temp = pd.read_csv(filename,  skiprows = 1, sep = ',',  header=None)
        self.__class__.ordinata_y_temp=y_temp[int(dc.get())]
        self.filtraggio()
        #ASCISSE:
        self.__class__.ordinata_x=np.arange(0,(len(self.__class__.ordinata_y_filtrata))/int(sf.get()),1/int(sf.get()))
        

            
#main
if __name__=='__main__':
    window=tk.Tk()
    finestra=window_Tk(window)
    finestra.costruzione_finestra()
    finestra.creazione_label('DATA COLUMN',100,170,'#f2bac7','dc',100,200)
    finestra.creazione_label('SKIP DATA',100,270,'#f2bac7','sd',100,300)
    finestra.creazione_label('POSSIBILE FILTERS',100,370,'#f2bac7','pf',100,400)
    finestra.creazione_label('HIGH FILTER',100,470,'#f2bac7','hf',100,500)
    finestra.creazione_label('LOW FILTER',100,570,'#f2bac7','lf',100,600)
    finestra.creazione_label('SAMPLE FREQUENCY',100,670,'#f2bac7','sf',100,700)
    
    finestra.creazione_bottoni('CARICA FILE DAL BROWSE',SUNKEN,'white','#f71d86','select_file',100,100)
    finestra.creazione_bottoni('CHIUDI',SUNKEN,'white','#f71d86','chiudi',1250,700)
    finestra.creazione_bottoni('CARICAMENTO DATI',SUNKEN,'white','#f71d86','verifica',750,700)
    finestra.creazione_bottoni('GRAFICO CON SEGNALE FILTRATO',SUNKEN,'white','#f71d86','disegna_grafico_filtrato',1050,700)
    finestra.creazione_bottoni('GRAFICO DELLO SPETTRO',SUNKEN,'white','#f71d86','disegna_grafico_spettro',890,700)

    
    window.mainloop()