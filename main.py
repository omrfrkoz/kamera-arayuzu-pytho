

from tkinter import filedialog, messagebox
import cv2
import serial
from tkinter import *
from tkinter.ttk import Combobox, Treeview
from PIL import ImageTk, Image
from zoom import zoom
import numpy as np
import os
import csv
import colorsys
import tkinter as tk

ports = ['COM%s' % (i + 1) for i in range(256)]      
portlar = []                                         #  PC ye bağlı olna Portları listeliyoruz
for port in ports:
    try:
        s = serial.Serial(port)
        s.close()
        portlar.append(port)
    except (OSError, serial.SerialException):
        pass

class TitleFrame(Frame):
    def __init__(self,window):
        super().__init__(window)
        self.pack()        # Bileşenleri ekrana bas
        self.GUI()      # GUİ yi Çağır
        self.kamera=0  # Kamera Switch 
        self.ardunio_select=0  # Servo Hareketi Switch
        self.serial_select=0 # Seri Bağlantı Switch
        self.ardunio = serial # ardunio bağlantısı
        self.posizyon=90        # Servo pozisyonu
        self.kalibre_aktif=0
        
    def GUI(self):
        #############################  FRAMELER  #############################
        self.f=Frame(self,bg="white")
        self.f.pack(fill=BOTH,expand=YES)

        self.frame1=Frame(self.f,width=1640,height=50,bg="white")
        self.frame1.pack()

        self.frame2=Frame(self.f,width=1640,height=480,bg="blue")
        self.frame2.pack()

        frame2_1=Frame(self.frame2,bg="black",width=640,height=480)
        frame2_1.pack(side=LEFT,anchor=E,fill=BOTH)


        canvas_frame2_2=Frame(self.frame2,bg="white",width=360,height=480)
        canvas_frame2_2.pack(side=LEFT,anchor=E,fill=BOTH)

        frame2_3 = Frame(self.frame2,bg="white",width=640,height=480)
        frame2_3.pack(side=LEFT,anchor=E,fill=BOTH)
        
        self.frame3_canvas = Canvas(frame2_3,bg="white",width=640,height=480)
        self.frame3_canvas.place(x=0,y=0)

        frame2_2 = Canvas(canvas_frame2_2,background="white",width=360,height=480)
        frame2_2.place(x=0,y=0)

        #Frame 1

        label1=Label(self.frame1,text="Kamera Arayüzü",font=('Helvetica bold',25),bg="white")
        label1.place(x=700,y=0)

        
        #Frame 2.1 


##########################################################  FONKSİYONLAR   ##########################################################
        cap= cv2.VideoCapture(0)     # WEB CAMERAYİ YAKALA
        canvas = Canvas(frame2_1,width=640,height=480)  # CANVAS OLUŞTUR
        canvas.place(x=0,y=0)                           # CANVASI EKRANDA YERLEŞTİR

        self.arayüz_renk = "#00067e"                    # DEFOULT ARAYÜZ RENGİ
        self.hud_renk = (0,255,0)                       # DEFOULT HUD RENGİ

        ############################ ARAYÜZ RENK DEĞİŞTİRME FONKSİYONU ##############################
        def arayüz_renk(renk):
            self.frame3_canvas.create_line(0,140,640,140, fill=(f"{self.arayüz_renk}"),width=4)
            self.frame3_canvas.create_line(0,320,640,320, fill=f"{self.arayüz_renk}",width=4)
            self.frame3_canvas.create_line(200,230,640,230, fill=f"{self.arayüz_renk}",width=4)
            self.frame3_canvas.create_line(200,140,200,320, fill=f"{self.arayüz_renk}",width=4)
            self.frame3_canvas.create_line(638,0,638,480, fill=f"{self.arayüz_renk}",width=4)
            self.frame3_canvas.create_line(430,140,430,411, fill=f"{self.arayüz_renk}",width=4)
            self.frame3_canvas.create_line(3,0,3,480, fill=f"{self.arayüz_renk}",width=4)
            self.frame3_canvas.create_line(0,100,640,100, fill=f"{self.arayüz_renk}",width=4)
            self.frame3_canvas.create_line(0,4,640,4, fill=f"{self.arayüz_renk}",width=4)
            self.frame3_canvas.create_line(0,478,640,478, fill=f"{self.arayüz_renk}",width=4)
            self.frame3_canvas.create_line(430,410,640,410, fill=f"{self.arayüz_renk}",width=4) 

            frame2_2.create_line(0,478,360,478, fill=f"{self.arayüz_renk}",width=4)
            frame2_2.create_line(0,4,360,4, fill=f"{self.arayüz_renk}",width=4)
            frame2_2.create_line(3,0,3,480, fill=f"{self.arayüz_renk}",width=4)
            frame2_2.create_line(360,0,360,480, fill=f"{self.arayüz_renk}",width=4)
            
            canvas.create_line(0,3,640,3, fill=f"{self.arayüz_renk}",width=4)
            canvas.create_line(3,0,3,480, fill=f"{self.arayüz_renk}",width=4)
            canvas.create_line(0,3,640,3, fill=f"{self.arayüz_renk}",width=4)
            canvas.create_line(0,477,640,477, fill=f"{self.arayüz_renk}",width=4)
        
            
        ############################  RGB KODUNA DÖNÜLŞTÜERME FONKSİYONU ############################
        def rgb_hack(rgb):
            return "#%02x%02x%02x" % rgb  
        ############################ CANVASDA FRAME GÖSTERME FONKSİYONU ############################
        def frame_göster():
            
        
            ####### HUD VE ARAYÜZ RENK İŞLEMLERİ########
            if (self.arayüz_sec.get()=="Kırmızı"):
                self.arayüz_renk = "red"
                arayüz_renk(self.arayüz_renk)
            if (self.arayüz_sec.get()=="Yeşil"):
                self.arayüz_renk = "green"
                arayüz_renk(self.arayüz_renk)
            if (self.arayüz_sec.get()=="Mavi"):
                self.arayüz_renk = "#00067e"
                arayüz_renk(self.arayüz_renk)
            if (self.arayüz_sec.get()=="Pembe"):
                self.arayüz_renk = "pink"
                arayüz_renk(self.arayüz_renk)
            if (self.arayüz_sec.get()=="Cyan"):
                self.arayüz_renk = "cyan"
                arayüz_renk(self.arayüz_renk)

            if (self.hud_sec.get()=="Kırmızı"):
                self.hud_renk = (255,0,0)
               
            if (self.hud_sec.get()=="Yeşil"):
                self.hud_renk = (0,255,0)
               
            if (self.hud_sec.get()=="Mavi"):
                self.hud_renk = (0,6,126)
                
            if (self.hud_sec.get()=="Pembe"):
                self.hud_renk = (255,51,122)
                
            if (self.hud_sec.get()=="Cyan"):
                self.hud_renk = (0,255,255)
                
            
                
            #############################################
            
            ############# KAMERA SWİTCH EĞER 0 İSE CANVASA GÖRÜNTÜYÜ BAS ###############
            if (self.kamera == 0):
                trackle_frame=0
                #######TRACK########## 
                if var_trackle.get() ==0:                                                                           # EĞER ARAYÜZDEN TRACK İPTAL SEÇİLİ İSE 
                    treeview1.insert("",index=0,values=(f"{trackbar1.get()}","","","","",f"{trackbar2.get()}"))     # TREEVİEW'E ŞU BİLGİLER YAZILSIN
                    if (self.ardunio_select==1):                                                                    # SERVO HAREKETİ SWİTCH'İ 1 İSE
                        self.ardunio_select=0                                                                       # SERVO HAREKETİ SWİTCH'İNİ 0 YAP
                        Servo()                                                                                     # SERVO FONKSİYONUNU ÇALIŞTIR
                if var_trackle.get() == 1 :                                                                         # ARATÜZDEN KIRMIZI SEÇİLİ İSE RENK ARALIKLARINI ŞU ŞEKİLDE AYARLA
                            low_renk = np.array([0, 120, 70])
                            high_renk = np.array([15, 240, 240])
                            l_h.set(0)
                            l_s.set(120)
                            l_v.set(70)
                      

                if var_trackle.get() == 2:                                                                          # ARATÜZDEN YEŞİL SEÇİLİ İSE RENK ARALIKLARINI ŞU ŞEKİLDE AYARLA
                            low_renk = np.array([30, 61, 50])
                            high_renk = np.array([100, 240, 240])
                            l_h.set(54)
                            l_s.set(61)
                            l_v.set(50)
                        


                if var_trackle.get() == 6:                                                                          # ARATÜZDEN TURUNCU  SEÇİLİ İSE RENK ARALIKLARINI ŞU ŞEKİLDE AYARLA

                            low_renk = np.array([10, 50, 70])
                            high_renk = np.array([24, 255, 255])
                            l_h.set(10)
                            l_s.set(50)
                            l_v.set(70)
                     
                if var_trackle.get()==4:                                                                            #  ARATÜZDEN SARI SEÇİLİ İSE RENK ARALIKLARINI ŞU ŞEKİLDE AYARLA
                            low_renk = np.array([25, 50, 70])
                            high_renk = np.array([35, 255, 255])
                            l_h.set(25)
                            l_s.set(50)
                            l_v.set(70)
                       
                if var_trackle.get()==5:                                                                            # ARATÜZDEN MAVİ SEÇİLİ İSE RENK ARALIKLARINI ŞU ŞEKİLDE AYARLA
                            low_renk = np.array([90, 50, 70])
                            high_renk = np.array([128, 255, 255])
                            l_h.set(90)
                            l_s.set(50)
                            l_v.set(70)

                r = 255     # DEFOULT RGB DEĞERİ
                g = 255
                b = 255

                if var_trackle.get() == 3:                                                                  #  ARATÜZDEN RENK SEÇ  SEÇİLİ İSE RENK ARALIKLARINI ŞU ŞEKİLDE AYARLA
                    (h,s,v) = (l_h.get()/255,l_s.get()/255,l_v.get()/255)                                   #  HSV KODUNU RGB YE ÇEVİR VE LABEL'A BG YAP
                    (r,g,b) = colorsys.hsv_to_rgb(h,s,v)
                    (r,g,b) = (int (r*255) ,int(g*255), int(b*255))
                    renkk= rgb_hack((r,g,b))
                    label15["bg"]= renkk
                    high_renk = np.array([l_h.get()+h_h.get(),255,255])                                     # VE RENK ARALIGINI AYARLA
                    low_renk = np.array([l_h.get()-h_h.get(),l_s.get()-h_h.get(),l_v.get()-h_h.get()])
                if var_trackle.get() != 0:                                                                  # ARAYÜZDEN TRACK SEÇİLİ İSE 
                            self.ardunio_select=1                                                           # Servo bağlantısını kes
                            _, frame = cap.read()                                                           # web cam'den frame'i al 
                            _, cols, _ = frame.shape                                                        # Frame'in stünunu hesapla 
                            center = int(cols / 2) 
                            x_medium = int(cols / 2)                                                        # ekranın ortasını bul
                            _, frame = cap.read()                                                           # web cam'den frame'i al                                  
                            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)                                   # gelen BGR görüntüyü RGB ye dönüştür.
                            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)                              #  RGB görüntüyü HSV ye dönüştür.
                            low_renk = low_renk                                                             # yukarıda seçtiğimiz renk aralıklarını tanımla
                            high_renk = high_renk
                            red_mask = cv2.inRange(hsv_frame, low_renk, high_renk)                          # renk aralıklarına göre görüntüyü maskele
                            _, threshd = cv2.threshold(red_mask,20, 255, cv2.THRESH_BINARY)                 # görüntütü binary grüntüuye dönüştür
                            contours, _ = cv2.findContours(threshd, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # conturları bul
                            contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)      #conturları küçükten büyüğe sırala
                            x=0
                            y=0
                            w=0                         # x y w h defoult değerleri
                            h=0
                            for cnt in contours:
                                (x, y, w, h) = cv2.boundingRect(cnt)         #  bulduğu counturun köşe noktalarını hesaplıyor
                                x_medium = int((w/ 2)+x)                     #  kare içine aldığı nesneni orta noktasını hesapla 
                                break
                            if ((w)<30):                               #  eğer karenin büyüklüğü 30 pikselden küçükse birşey yapma 
                                    pass
                            else:
                                if x_medium < center -30:               # karenin orta noktası , ekranın orta noktasından  sola doğru kayarsa pozisyonu bir arttır
                                    self.posizyon += 1
                                elif x_medium > center + 30:            # karenin orta noktası , ekranın orta noktasından  sağa doğru kayarsa pozisyonu bir azalt
                                    self.posizyon -= 1
                                if self.posizyon<=1:                    # servo motor 1-180 derece arası değer alabildiği için sınırlama
                                    self.posizyon=1
                                elif self.posizyon>=180:
                                    self.posizyon=180
                                treeview1.insert("",index=0,values=(f"{trackbar1.get()}",f"{x}",f"{x+w}",f"{y}",f"{y+h}",f"{trackbar2.get()}"))  # treeview de şu bilgileri yaz
                                cv2.rectangle(frame,(x , y),(x+w,y+h),(self.hud_renk),2)    # nesneyi kare içine al 
                            cv2.putText(frame, f"pos= {self.posizyon} ", (30,20),cv2.FONT_HERSHEY_SIMPLEX, 1, (self.hud_renk), 1)  # ekrana pozisyon bilgisini yaz  
                            frame = cv2.resize(frame , (640,480))
                            trackle_frame = frame  
                            b = self.posizyon.to_bytes(2,"little")                             # pozisyon bilgisini byte' a dönüştür
                            self.ardunio.write(b)                                              # ardunioya byte olarak pozisyonu gönder
                            trackbar1.set(self.posizyon)                                        # trackbar1 ' i pozisyon değerine ata
                
                zoom(self,cap.read(),trackbar2.get(),canvas,var_nesne.get(),var_trackle.get(),var_histogram.get(),var_gamma.get(),trackbar3.get(),trackle_frame,trackbar4.get(),var_brightness.get(),var_kontast.get(),trackbar5.get(),trackbar6.get(),trackbar7.get(),trackbar8.get(),var_sharpness.get(),self.hud_renk,var_color.get(),trackbar9.get())  # zoom fonksiyonunu çağır
                trackbar2.after(24,frame_göster) # 24 ms de bir frame_göster fonksiyonunu çalıştır.
        ##################### Servo hareketi fonksiyonu ########################         
        def Servo():  
            if (self.ardunio_select==0):# eğer a = 0 ise servo hareketi çalışsın
                command = int(trackbar1.get()) 
                b = command.to_bytes(2,"little")
                self.ardunio.write(b)
                self.posizyon=trackbar1.get()
                trackbar2.after(24,Servo)
        #############################################        

        ################### Treevievdeki bilgileri kaydetme fonksiyonu ##########################
        def Tree_kaydet():
            if (len(treeview1.get_children())<1):
                messagebox.showinfo("Veri Yok","Kaydedilecek Veri Bulunamadı")
            file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title = "Kaydet", filetypes=(("CSV File","*.csv"),("All Files","*.*"))) 
            with open (file , mode="w", newline="")as myfile:
                exp_writer = csv.writer(myfile,delimiter='\t')
                exp_writer.writerow(["Servo Pozisyonu","X1","X2","Y1","Y2","Zoom"])
                for i in treeview1.get_children():
                    degerler = treeview1.item(i)["values"]
                    exp_writer.writerow(degerler)
        ##########################################################################################

        ##################### Durdur Buton Fonskiyonu ########################
        def Quitt():
            self.kamera=1
            self.ardunio_select=1
        ####################### COM seçince çalışacak olan fonksiyon ######################
        def Baslat():
            if (self.serial_select == 0):
                self.ardunio = serial.Serial(self.com_sec.get(), 9600) # ARDUNİO BAĞLANTI KURMA
            self.serial_select=1
            self.kamera=0
            self.ardunio_select=0
            frame_göster()
            Servo()
       
        


        #############################################################################################################################################################
       
        #Frame 2.2 

        
        self.arayüz_sec=StringVar()
        self.arayüz_sec.set("Arayüz Rengi")
        
        self.combobox2=Combobox(frame2_2,textvariable=self.arayüz_sec,state="readonly",values=["Kırmızı","Yeşil","Mavi","Pembe","Cyan"],width=12,height=5)
        self.combobox2.place(x=200,y=20)


        self.hud_sec=StringVar()
        self.hud_sec.set("Hud Rengi")
        
        self.combobox2=Combobox(frame2_2,textvariable=self.hud_sec,state="readonly",values=["Kırmızı","Yeşil","Mavi","Pembe","Cyan"],width=10,height=5)
        self.combobox2.place(x=100,y=20)





        self.com_sec=StringVar()
        self.com_sec.set("Com Seç")
        
        self.combobox2=Combobox(frame2_2,textvariable=self.com_sec,state="readonly",values=portlar,width=10,height=2)
        self.combobox2.place(x=10,y=20)
        self.combobox2.bind("<<ComboboxSelected>>", lambda event: Baslat())

        Button9 = Button(frame2_2,text="Durdur",command=Quitt,height=1,bg="white")
        Button9.place(x=300,y=20)



        label3=Label(frame2_2,text="Servo Kontrol",font=('Helvetica bold',12),bg="white")
        label3.place(x=130,y=45)
        trackbar1=Scale(frame2_2,from_=0 , to=180,orient= HORIZONTAL,length=330,bg="white")
        trackbar1.set(90)
        trackbar1.place(x=10,y=65)
        
        label3=Label(frame2_2,text="Zoom",font=('Helvetica bold',12),bg="white")
        label3.place(x=150,y=115)
        trackbar2=Scale(frame2_2,from_=0 , to=50,orient= HORIZONTAL,length=330,bg="white")
        trackbar2.place(x=10,y=140)
        
        columns = ("s_pozisyon","x_poziyon","x2","y_pozisyon","y2","Zoom")
        treeview1 = Treeview(frame2_2,columns=columns,show="headings",height=10)
        treeview1.column("#1",anchor=CENTER,stretch=NO,width=100)
        treeview1.column("#2",anchor=CENTER,stretch=NO,width=40)
        treeview1.column("#3",anchor=CENTER,stretch=NO,width=40)
        treeview1.column("#4",anchor=CENTER,stretch=NO,width=40)
        treeview1.column("#5",anchor=CENTER,stretch=NO,width=40)
        treeview1.column("#6",anchor=CENTER,stretch=NO,width=75)
        treeview1.heading('s_pozisyon', text='Servo Pozisyon')
        treeview1.heading('x_poziyon', text='X1')
        treeview1.heading('x2', text='X2')
        treeview1.heading('y2', text='Y2')
        treeview1.heading('y_pozisyon', text='Y1')
        treeview1.heading('Zoom', text='Zoom')
        treeview1.place(x=10,y=180)




        Button1 = Button(frame2_2,text="Kaydet",width=20,command= Tree_kaydet)
        Button1.place(x=10,y=410)

        Button2 = Button(frame2_2,text="Kapat",command=my_window.destroy,width=20)
        Button2.place(x=190,y=410)

        #Frame 3
        ###################### Renk Seç butonuna tıklayınca çalışan fonksiyon #######################
        def renk_sec():
            def TiklamaOlayi(olay, x, y, flags, param):
                if olay == cv2.EVENT_LBUTTONDOWN:
                    r = rgb[y, x, 0]
                    g = rgb[y, x, 1]
                    b = rgb[y, x, 2]
                    h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
                    l_h.set(int(h*255))
                    l_s.set(int(s*255))
                    l_v.set(int(v*255))
                    cv2.imshow("Goruntu", goruntu)
                    cv2.destroyAllWindows()
            _,goruntu = cap.read()
            goruntu = cv2.resize(goruntu , (800,600))
            rgb = cv2.cvtColor(goruntu, cv2.COLOR_BGR2RGB)
            cv2.imshow("Goruntu", goruntu)
            cv2.setMouseCallback('Goruntu',TiklamaOlayi)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
       
        renkbutton = Button(self.frame3_canvas,text="Renk Seç",command=renk_sec)
        renkbutton.place(x=100,y=430)


        var_nesne = IntVar()
        radiaobutton1=Radiobutton(self.frame3_canvas,text="İnsan",bg="white",variable=var_nesne,value= 1)
        radiaobutton1.place(x=20,y=110)

        radiaobutton2=Radiobutton(self.frame3_canvas,text="Araba",bg="white",variable=var_nesne,value= 2)
        radiaobutton2.place(x=140,y=110)

        radiaobutton3=Radiobutton(self.frame3_canvas,text="Telefon",bg="white",variable=var_nesne,value= 3)
        radiaobutton3.place(x=260,y=110)

        radiaobutton15=Radiobutton(self.frame3_canvas,text="Hepsi",bg="white",variable=var_nesne,value= 4)
        radiaobutton15.place(x=380,y=110)


        radiaobutton4=Radiobutton(self.frame3_canvas,text="İptal",bg="white",variable=var_nesne,value= 0)
        radiaobutton4.place(x=500,y=110)
        


        var_trackle=IntVar()

        radiaobutton5=Radiobutton(self.frame3_canvas,text="Kırmızı",bg="white",variable=var_trackle,value= 1)
        radiaobutton5.place(x=20,y=330)

       
        radiaobutton7=Radiobutton(self.frame3_canvas,text="Yeşil",bg="white",variable=var_trackle,value= 2)
        radiaobutton7.place(x=20,y=360)


        radiaobutton6=Radiobutton(self.frame3_canvas,text="Renk Seç",bg="white",variable=var_trackle,value= 3)
        radiaobutton6.place(x=100,y=390)

        radiaobutton6=Radiobutton(self.frame3_canvas,text="Sarı",bg="white",variable=var_trackle,value= 4)
        radiaobutton6.place(x=100,y=330)

        radiaobutton6=Radiobutton(self.frame3_canvas,text="Mavi",bg="white",variable=var_trackle,value= 5)
        radiaobutton6.place(x=100,y=360)

        radiaobutton6=Radiobutton(self.frame3_canvas,text="Turuncu",bg="white",variable=var_trackle,value= 6)
        radiaobutton6.place(x=20,y=390)
        radiaobutton66=Radiobutton(self.frame3_canvas,text="iptal",bg="white",variable=var_trackle,value= 0)
        radiaobutton66.place(x=20,y=420)
                


        var_histogram = IntVar()
        radiaobutton3=Radiobutton(self.frame3_canvas,text="Histogram eşitleme",bg="white",variable=var_histogram,value=1)
        radiaobutton3.place(x=20,y=150)
        radiaobutton6=Radiobutton(self.frame3_canvas,text="Histogram eşitleme İptal",bg="white",variable=var_histogram,value=0)
        radiaobutton6.place(x=20,y=180)
        trackbar6=Scale(self.frame3_canvas,from_=1 , to=10,orient= HORIZONTAL,length=100,bg="white")
        trackbar6.set(2)
        trackbar6.place(x=75,y=220)
        trackbar7=Scale(self.frame3_canvas,from_=1 , to=10,orient= HORIZONTAL,length=100,bg="white")
        trackbar7.set(4)
        trackbar7.place(x=75,y=270)
        label7=Label(self.frame3_canvas,text="Tile X-Y",bg="white")
        label7.place(x=20,y=225)
        label8=Label(self.frame3_canvas,text="Clip Limit",bg="white")
        label8.place(x=20,y=280)



        var_brightness = IntVar()
        radiaobutton9=Radiobutton(self.frame3_canvas,text="Parlaklık",bg="white",variable=var_brightness,value=1)
        radiaobutton9.place(x=230,y=150)
        radiaobutton10=Radiobutton(self.frame3_canvas,text="Parlaklık İptal",bg="white",variable=var_brightness,value=0)
        radiaobutton10.place(x=300,y=150)

        trackbar4=Scale(self.frame3_canvas,from_=1 , to=50,orient= HORIZONTAL,length=150,bg="white")
        trackbar4.set(10)
        trackbar4.place(x=230,y=180)


        var_sharpness = IntVar()
        radiaobutton16=Radiobutton(self.frame3_canvas,text="Keskinlik",bg="white",variable=var_sharpness,value=1)
        radiaobutton16.place(x=450,y=240)
        radiaobutton17=Radiobutton(self.frame3_canvas,text="Keskinlik İptal",bg="white",variable=var_sharpness,value=0)
        radiaobutton17.place(x=520,y=240)


        var_color = IntVar()
        radiaobutton19=Radiobutton(self.frame3_canvas,text="Renk Değeri",bg="white",variable=var_color,value=1)
        radiaobutton19.place(x=450,y=330)
        radiaobutton18=Radiobutton(self.frame3_canvas,text="İptal",bg="white",variable=var_color,value=0)
        radiaobutton18.place(x=550,y=330)
        
        trackbar9=Scale(self.frame3_canvas,from_=1 , to=50,orient= HORIZONTAL,length=150,bg="white")
        trackbar9.set(10)
        trackbar9.place(x=450,y=360)

        
        trackbar8=Scale(self.frame3_canvas,from_=1 , to=50,orient= HORIZONTAL,length=150,bg="white")
        trackbar8.set(10)
        trackbar8.place(x=450,y=270)


        var_kontast = IntVar()
        radiaobutton11=Radiobutton(self.frame3_canvas,text="Kontrast",bg="white",variable=var_kontast,value=1)
        radiaobutton11.place(x=230,y=240)
        radiaobutton12=Radiobutton(self.frame3_canvas,text="Kontrast iptal",bg="white",variable=var_kontast,value=0)
        radiaobutton12.place(x=300,y=240)

        trackbar5=Scale(self.frame3_canvas,from_=1 , to=50,orient= HORIZONTAL,length=150,bg="white")
        trackbar5.set(10)
        trackbar5.place(x=230,y=270)



        var_gamma=IntVar()
        radiaobutton5=Radiobutton(self.frame3_canvas,text="Gama",bg="white",variable=var_gamma,value=1)
        radiaobutton5.place(x=450,y=150)
        radiaobutton8=Radiobutton(self.frame3_canvas,text="Gama İptal",bg="white",variable=var_gamma,value=0)
        radiaobutton8.place(x=520,y=150)
        
        trackbar3=Scale(self.frame3_canvas,from_=1 , to=50,orient= HORIZONTAL,length=150,bg="white")
        trackbar3.set(10)
        trackbar3.place(x=450,y=180)


        l_h=Scale(self.frame3_canvas,from_=1 , to=255,orient= HORIZONTAL,length=150,bg="white")
        l_h.set(0)
        l_h.place(x=230,y=330)
        label9=Label(self.frame3_canvas,text="LH",bg="white")
        label9.place(x=200,y=340)

        
        l_s=Scale(self.frame3_canvas,from_=1 , to=255,orient= HORIZONTAL,length=150,bg="white")
        l_s.set(0)
        l_s.place(x=230,y=370)
        label10=Label(self.frame3_canvas,text="LS",bg="white")
        label10.place(x=200,y=380)

        l_v=Scale(self.frame3_canvas,from_=1 , to=255,orient= HORIZONTAL,length=150,bg="white")
        l_v.set(0)
        l_v.place(x=230,y=410)
        label11=Label(self.frame3_canvas,text="LV",bg="white")
        label11.place(x=200,y=420)

        h_h=Scale(self.frame3_canvas,from_=1 , to=100,orient= HORIZONTAL,length=150,bg="white")
        h_h.set(40)
        h_h.place(x=470,y=420)
        label12=Label(self.frame3_canvas,text="Aralık",bg="white")
        label12.place(x=420,y=430)


         
        logo = Image.open("logo1.png")
        logo=logo.resize((350,75),Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        label20=Label(self.frame3_canvas, image=logo,bg="white")
        label20.image = logo
        label20.place(y=7,x=150)

  

       
        label15=Label(self.frame3_canvas,bg="white",text="            ")
        label15.place(x=400,y=450)
        # Frame Cizgileri

        self.frame3_canvas.create_line(0,140,640,140, fill=(f"{self.arayüz_renk}"),width=4)
        self.frame3_canvas.create_line(0,320,640,320, fill=f"{self.arayüz_renk}",width=4)
        self.frame3_canvas.create_line(200,230,640,230, fill=f"{self.arayüz_renk}",width=4)
        self.frame3_canvas.create_line(200,140,200,320, fill=f"{self.arayüz_renk}",width=4)
        self.frame3_canvas.create_line(638,0,638,480, fill=f"{self.arayüz_renk}",width=4)
        self.frame3_canvas.create_line(430,140,430,411, fill=f"{self.arayüz_renk}",width=4)
        self.frame3_canvas.create_line(3,0,3,480, fill=f"{self.arayüz_renk}",width=4)
        self.frame3_canvas.create_line(0,100,640,100, fill=f"{self.arayüz_renk}",width=4)
        self.frame3_canvas.create_line(0,4,640,4, fill=f"{self.arayüz_renk}",width=4)
        self.frame3_canvas.create_line(0,478,640,478, fill=f"{self.arayüz_renk}",width=4)
        self.frame3_canvas.create_line(430,410,640,410, fill=f"{self.arayüz_renk}",width=4) 

        frame2_2.create_line(0,478,360,478, fill=f"{self.arayüz_renk}",width=4)
        frame2_2.create_line(0,4,360,4, fill=f"{self.arayüz_renk}",width=4)
        frame2_2.create_line(3,0,3,480, fill=f"{self.arayüz_renk}",width=4)
        frame2_2.create_line(360,0,360,480, fill=f"{self.arayüz_renk}",width=4)
        
        canvas.create_line(0,3,640,3, fill=f"{self.arayüz_renk}",width=4)
        canvas.create_line(3,0,3,480, fill=f"{self.arayüz_renk}",width=4)
        canvas.create_line(0,3,640,3, fill=f"{self.arayüz_renk}",width=4)
        canvas.create_line(0,477,640,477, fill=f"{self.arayüz_renk}",width=4)
        
        
        


my_window=Tk()

frame_a=TitleFrame(my_window)
my_window.geometry("1640x530")
my_window.title(" Kamera Arayüzü - Ömer Faruk ÖZYILMAZ - Elektro Optik Sistemler ")
my_window.resizable(False, False)
my_window.wm_iconbitmap("kaos4.ico")
my_window.mainloop()
