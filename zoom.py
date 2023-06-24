
import cv2
from PIL import ImageTk, Image,ImageEnhance,ImageFilter
import tkinter as tk
import numpy as np
from nesne_tespit import nesne_takip





def zoom(self,cap,tracbar2,cc,var_nesne,value_trackle,var_histogram,var_gamma,var_trackbar3,trackle_frame,trackbar4,var_brightness,var_kontrast,trackbar5,trackbar6,trackbar7,trackbar8,var_sharpness,hud_renk,var_color,trackbar9_color):
        ############################# Frame Alma #######################################################################################
        _,self.frame = cap                                              # cap = cap.read()    Frame alma 
        self.frame=cv2.resize(self.frame,(640,480))                     # Alınan Frame'i Canvas'ın çözünürlüğüne dönüştürme
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)        # Alınan BGR Frame'i RGB ye dönüştürme 

        #################################################################################################################################    
        #############################   Nesne Takip Seçenekleri    ######################################################################
        nesne = 0
        if var_nesne == 1:
            nesne = "insan"                               
        if var_nesne == 2:                                  #  Burada kullanıcı arayüzden, nesne tespit alanından seçtiği nesneyi
            nesne ="araba"                              #  nesne değerine atıyor ve bu nesne değerini nesne_takip fonksiyonuna gönderiyoruz
        if var_nesne == 3:                                  
            nesne ="telefon"                            
        if var_nesne == 4:                                   
            nesne ="hepsi"                              
        if (nesne!=0):                                  # eğer nesne değeri 0 dan farklı ise nesne_takip çalışsın
                self.frame =nesne_takip(cap,nesne,hud_renk)       
                
        #########################################################################################################################################


        ######################################### Tracden gelen frame'yi ekranda bastırma için atamalar #########################################
       
        if value_trackle != 0 :                 # value_trackle = var_trackle    trackle_frame = takip seçeneğinden çıkan frame görüntüsü 
                self.frame = trackle_frame      # tracle_frame i canvasda bastırmak için self.frame değerine atadık.
      
       ###########################################################################################################################

                
        ######################################### Contrast limited apadatif histogram equ #########################################
        if(var_histogram==1):
                clahe = cv2.createCLAHE(clipLimit=trackbar7,tileGridSize=(trackbar6,trackbar6))   # Clahe oluşturmak lazım olan 2 değeri, arayüzden alıp buraya atadık 
                r = clahe.apply(self.frame[:, :, 0])                                              # self.frame'in her ayrı kanala claheyi uyguladık                                                                              
                g = clahe.apply(self.frame[:, :, 1])
                b = clahe.apply(self.frame[:, :, 2])
                self.frame = cv2.merge((r,g,b))                                                   # her bir kanalı birleştir.
                cv2.putText(self.frame, f"Histogram Esitleme Acik", (120,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, hud_renk, 2)
        ###########################################################################################################################



        #########################################    Gamma     ##################################################################################
        if (var_gamma==1):
            var_trackbar3=var_trackbar3/10                                                                                      # gamma değerini trackbar3 den al
            gamma_frame = np.array([((i / 255.0) ** (1/var_trackbar3)) * 255 for i in np.arange(0, 256)]).astype("uint8")       # s=cr^(1/i)  formülünden gama tablosu oluşturuyouruz
            self.frame= cv2.LUT(self.frame, gamma_frame)                                                                        # s = çıkış pikseli c = 255  r = (1:255)/255   i = gamma degeri
                                                                                                                                # Oluşturulan gama tablosu ile self.frame frameini işliyor (look up table)
        
            cv2.putText(self.frame, f"Gamma= {var_trackbar3} ", (0,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, hud_renk, 2)
        ################################################################################################################################################



        ######################################### Parlaklık Değer Atama  ###############################################################################
        factor_brightness=1                                     # factor = 1 olursa görüntüye parlaklık uygulamaz
        if (var_brightness == 1):                               # kullanıcı arayüzden parlaklığı aktif ederse döngüye girsin       g(i,j) = a*f(i,j)+b
                factor_brightness = trackbar4/10                # factor değerini trackbar4 den al
                cv2.putText(self.frame, f"Parlaklik= {factor_brightness} ", (350,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, hud_renk, 2)   # Ekranda parlaklık değerini göster 
        ####################################################################################################################################################################

      
        
        #########################################  Kontrast Değer Atama ##################################################################################
        factor_contrast=1                                         # factor = 1 olursa görüntüye kontrast uygulamaz
        if (var_kontrast == 1):                                   # kullanıcı arayüzden kontrastı aktif ederse döngüye girsin
                factor_contrast = trackbar5/10                    # factor değerini trackbar5 den al
                cv2.putText(self.frame, f"Kontast= {factor_contrast} ", (500,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, hud_renk, 2)    # Ekranda parlaklık değerini göster 
        ###################################################################################################################################################



        ######################################### Keskinlik Değer Atama  ##################################################################################
        factor_sharpness=1                                               # factor = 1 olursa görüntüye keskinlik uygulamaz
        if (var_sharpness == 1):                                         # kullanıcı arayüzden keskinlik aktif ederse döngüye girsin
                factor_sharpness = trackbar8/10                          # factor değerini trackbar5 den al
                cv2.putText(self.frame, f"Keskinlik= {factor_sharpness} ", (0,50),cv2.FONT_HERSHEY_SIMPLEX, 0.5, hud_renk, 2)    # Ekranda parlaklık değerini göster 
        ####################################################################################################################################################

        

        ######################################### Renk Değer Atama  ##################################################################################
        factor_color=1                                               # factor = 1 olursa görüntüye keskinlik uygulamaz
        if (var_color == 1):                                         # kullanıcı arayüzden Renk değerini aktif ederse döngüye girsin
                factor_color = trackbar9_color/10                          # factor değerini trackbar5 den al
                cv2.putText(self.frame, f"Renk = {factor_color} ", (0,75),cv2.FONT_HERSHEY_SIMPLEX, 0.5, hud_renk, 2)    # Ekranda parlaklık değerini göster 
        ####################################################################################################################################################
                
      
        #########################################   ZOOM Ayarlama   ##################################################################################
        x1= int(0+(tracbar2*4))                                         # Ekran çözünürlüğü 4:3 oldugu için x ekseninden, trackbar2 den alınan değerin 4 katı artıp      
        y2 = int(480-(tracbar2*3))                                      # 4 katı azalması , y ekseninde ise 3 katı artıp azalması işlemini yap 
        y1 = int (0+(tracbar2*3))
        x2 = int (640-(tracbar2*4))
        self.frame = cv2.resize(self.frame[y1:y2,x1:x2],(640,480))      # self.frame de istenilen piksel aralıklarını al ve 640x480 çözünürlüğüne getir

        ##########################################################################################################################################################

        ######################################### Ekrana Görüntü Bastırma ########################################################################################

        self.frame = Image.fromarray(self.frame) # Gelen Frame'i PIL formatına dönüştür
        
        self.frame = ImageEnhance.Brightness(self.frame)        # Frame'e Atadığımız değerde parlaklık uygular
        self.frame = self.frame.enhance(factor_brightness)      # 
        self.frame = ImageEnhance.Sharpness(self.frame)         # Frame'e Atadığımız değerde keskinlik uygular
        self.frame = self.frame.enhance(factor_sharpness)       # 
        self.frame = ImageEnhance.Contrast(self.frame)          # Frame'e Atadığımız değerde kontrast uygula 
        self.frame = self.frame.enhance(factor_contrast)
        self.frame = ImageEnhance.Color(self.frame)             # Frame'e Atadığımız değerde Color Saturation uygula 
        self.frame = self.frame.enhance(factor_color)        
        self.frame = ImageTk.PhotoImage(self.frame)             # Görüntüyü tkinterda widgetlara(Canvas) resim ekleyebilmek için kullanılan obje olan Photoİmage formatına dönüştürdük
        cc.create_image(0, 0, anchor=tk.NW, image=self.frame)   # Frame'i canvas da ekanda göster
        
        ####################################################################################################################################################################

