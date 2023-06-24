import cv2
import numpy as np
def nesne_takip (cap,nesne,hud_renk): 
    net=cv2.dnn.readNet('yolov3-tiny.weights','yolov3-tiny.cfg')      #  weights(eğitilmiş obje dosyası) ve cfg(ayarlar dosyası) dosyasını okur 
    nesneler=[]                                                       #  Nesneler adında liste oluştur
    with open("coco.names",'r') as f:                                 #  coco.names içinde bulunan classları nesneler listesine ekle 
        nesneler= f.read().split('\n')
    _, img = cap                                                      #  cap = cap.read() /// frame al 
    img=cv2.cvtColor(cap[1], cv2.COLOR_BGR2RGB)                         # Gelen BGR görüntüyü RGB ye dönüştür
    img = cv2.resize(img, None, fx=1, fy=1)                             # gelen görüntüyünün boyunutu değiştir
    height, width, _= img.shape                                         # frame'in çözünürlüğünü öğren
    blob=cv2.dnn.blobFromImage(img,1/150, (416,416), (0,0,0), swapRB=True, crop=False)  # gelen frame'i 4 boyutlu blob oluşturur
    net.setInput(blob)                                                   
    ln = net.getLayerNames()                                            
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
    layerOutputs=net.forward(ln)
    boxes=[]
    confidences=[]
    class_ids=[]
    for output in layerOutputs:
        for detection in output:
            scores = detection[5::]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes= cv2.dnn.NMSBoxes(boxes, confidences,0.3,0.4)
    font=cv2.FONT_HERSHEY_PLAIN
    if len(indexes)>0:
        for i in indexes.flatten():

            x, y, w, h = boxes[i]
            label=str(nesneler[class_ids[i]])
            if label == nesne:
                confidence=str(round(confidences[i],2))
                cv2.rectangle(img,(x,y),(x+w,y+h),hud_renk,2)
                cv2.putText(img,label+" "+confidence,(x,y-5),font,1,(255,255,255),1)
            if nesne == "hepsi":
                confidence=str(round(confidences[i],2))
                cv2.rectangle(img,(x,y),(x+w,y+h),hud_renk,2)
                cv2.putText(img,label+" "+confidence,(x,y-5),font,1,(255,255,255),1)
    img = cv2.resize(img,(640,480))
    return img  