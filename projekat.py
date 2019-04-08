import numpy as np
import cv2  # OpenCV biblioteka
import matplotlib
import matplotlib.pyplot as plt
from knn import getKNN
from detekcija_prelaska import sabiranje

knn = getKNN()

f=open("out.txt", "w+")
f.write("RA 7/2015 Jelena Surlan\n")
f.write("file\tsum\n")
f.close()

for i in range(0, 10):
    video_url = 'data/video-' + str(i) + '.avi'
    print(video_url)

    video = cv2.VideoCapture(video_url)
    ret_val, frejm = video.read()
    frejm_rgb = cv2.cvtColor(frejm, cv2.COLOR_BGR2RGB)   

    #izdvajanje plavog kanala - linija
    frejm_rgb[:, :, 0] = 0 #stavlja crveni [0] kanal na 0 
    frejm_rgb[:, :, 1] = 0 #stavlja zeleni [1] kanal na 0 
       
    #frejm_sivi = cv2.cvtColor(frejm_rgb, cv2.COLOR_RGB2GRAY)
    # ivice linije
    plave_ivice = cv2.Canny(frejm_rgb, 0, 200)    

    #vraca koordinate linije
    plava_linija = cv2.HoughLinesP(plave_ivice, 1, np.pi / 180, 50, None, 180, 10)
    # print("plava linija: ", plava_linija)

    # oznacava liniju crvenom bojom
    for x1,y1,x2,y2 in plava_linija[0]:
        cv2.line(frejm_rgb, (x1,y1), (x2,y2), (255,0,0), 2)
        plava_linijaX1 = x1
        plava_linijaY1 = y1
        plava_linijaX2 = x2
        plava_linijaY2 = y2
        break # uzima se samo prva linija na koju se naidje

    #plt.imshow(frejm_rgb)
    #plt.show()
    # izdvajanje zelenog kanala - tackice
    novi_frejm = cv2.cvtColor(frejm, cv2.COLOR_BGR2RGB)
    novi_frejm[:, :, 2] =  0

    frejm_sivi = cv2.cvtColor(novi_frejm, cv2.COLOR_RGB2GRAY)

    # pretvaranje u binarnu sliku
    ret, binarna_slika = cv2.threshold(frejm_sivi, 50, 255, cv2.THRESH_BINARY)

    # 2, 2 (1) 2 2 (1)
    kernel_erozija = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    kernel_dilacija = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    #kernel = np.ones((2, 2), np.uint8)
    frejm_e = cv2.erode(binarna_slika, kernel_erozija, iterations=1)
    frejm_d = cv2.dilate(frejm_e, kernel_dilacija, iterations=2)
    slika, konture, hijerarhija = cv2.findContours(frejm_d, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    konture_brojevi = [] # ovde ce biti samo konture koje pripadaju
    for kontura in konture: # za svaku konturu
        (x, y, w, h) = cv2.boundingRect(kontura) # pronadji pravougaonik minimalne povrsine koji ce obuhvatiti celu konturu
        povrsina = cv2.contourArea(kontura)
        if h >= 10 and h <= 50 and povrsina > 90 and povrsina < 1000:
            odsecena = frejm_sivi[y:y+h, x:x+w]
            uvecana = cv2.resize(odsecena, (28, 28))  

            #cv2.rectangle(frejm_rgb,(x,y),(x+w,y+h),(0,255,0),2)
            #print(int(knn.predict(uvecana.reshape(1, 784))))
            #plt.imshow(uvecana, 'gray')
            #plt.show()
                         
            konture_brojevi.append(kontura) # ova kontura pripada bar-kodu

    print('Ukupan broj regiona: %d' % len(konture_brojevi))
    
    #cv2.drawContours(frejm_rgb, konture_brojevi, -1, (255, 0, 0), 1)
    #plt.imshow(frejm_rgb)
    #plt.show()

    linija = [(plava_linijaX1, plava_linijaY1), (plava_linijaX2, plava_linijaY2)]

    suma = sabiranje(video_url, linija, knn)

    f=open("out.txt", "a+")
    f.write(video_url + "\t" + str(suma) + "\n")
    f.close()    