import cv2 as cv
import numpy as np
from scipy import ndimage
import math
import matplotlib.pyplot as plt
from kontura import Kontura
from pomocna import presek

import copy

id_konture = -1 # globalni brojac koji sluzi kao id svake konture

def sledeci():
    global id_konture
    id_konture += 1 # uvecavam za svaku narednu konturu
    return id_konture

def u_blizini(izabrana_kontura, konture):
    ret_val = []
    for k in konture:
        # koordinate centra jedne konture
        x1 = int(k.poslednji_centar[0])
        y1 = int(k.poslednji_centar[1])

        # koordinate centra u odnosu na koju trazim konture u blizini        
        x2 = int(izabrana_kontura['centar'][0])
        y2 = int(izabrana_kontura['centar'][1])
        
        distanca = math.sqrt( (x2-x1)**2 + (y2-y1)**2 ) # distanca izmedju gornje dve tacke 
        if(distanca < 14):  # 19, 15 14
            ret_val.append(k)
    return ret_val

def sabiranje(video_putanja, linija, knn):
    snimak = cv.VideoCapture(video_putanja) # ucitavanje snimka

    pronadjeni_objekti = []
    zbir = 0

    while(snimak.isOpened()): # prolazak kroz sve frejmove
        ret, frejm = snimak.read() # uzimam jedan frejm
        
        if ret:
            donja_granica = np.array([231, 231, 231]) # [231, 231, 231]
            gornja_granica = np.array([254, 254, 255]) # [254, 254, 255]
            binarna_slika = cv.inRange(frejm, donja_granica, gornja_granica) # pretvaranje u binarnu sliku, sve sto je iznad 231 postace belo, a sve ispod 231 postace crno
            # plt.imshow(binarna_slika, 'gray')
            # plt.show()
            kernel = np.ones((2, 2)) # 2,2
            #kernel = cv.getStructuringElement(cv.MORPH_CROSS, (2, 2))          
            dilacija = cv.dilate(binarna_slika, kernel, iterations = 2)
            #cv.imshow('dilacija', dilacija)
            #cv.waitKey(0) 
            osobine_slike, broj_objekata = ndimage.label(dilacija)
            konture = ndimage.find_objects(osobine_slike) # pronadje konture

            for x in range(broj_objekata):
                kontura = konture[x] # uzimam jednu konturu od pronadjenih kontura

                # x i y centra konture, sirina i visina konture
                (cX, cY) = ((kontura[1].stop + kontura[1].start) // 2, (kontura[0].stop + kontura[0].start) // 2)
                (sirina, visina) = ( kontura[1].stop - kontura[1].start,  kontura[0].stop - kontura[0].start)
    
                if (sirina > 13 or visina > 10): # 10, 10
                    # pravim objekat izabrana kontura kojem se pridruzuje atribut 'centar' koji je uredjeni par 
                    # tj.  kordinate centra
                    izabrana_kontura = {'centar' : (cX, cY)}
                    
                    u_okolini = u_blizini(izabrana_kontura, pronadjeni_objekti)
                
                    if(len(u_okolini) == 0): # novi objekat - u pronadjene objekte se dodaje ta izabrana
                        odseceno = dilacija[cY-visina//2 : cY+visina//2, cX-sirina//2 : cX+sirina//2] # pravim malu slicicu
                        sirina_buffer = 0
                        visina_buffer = 0
                        if sirina < 28:
                            # koliko da se doda sa svake strane po sirini
                            sirina_buffer = int((28 - sirina) / 2)
                        if visina < 28:
                            # koliko da se doda sa svake strane po visini
                            visina_buffer = int((28 - visina) / 2)

                        # pravljenje crnog okvira    
                        uvecana = cv.copyMakeBorder(odseceno, visina_buffer, visina_buffer + ((28-visina) % 2), sirina_buffer, sirina_buffer + ((28-sirina) % 2), cv.BORDER_CONSTANT, value=[0,0,0])
                        uvecana = cv.resize(uvecana, (28, 28))
                        nova_kontura = Kontura(sledeci(), False, izabrana_kontura['centar'], uvecana)
                        pronadjeni_objekti.append(nova_kontura) # pronadjena kontura se dodaje u listu pronadjenih objekata
                    
                    if(len(u_okolini) == 1): # pracenje konture                  
                        najbliza = u_okolini[0] # najbliza kontura
                        najbliza.poslednji_centar = izabrana_kontura['centar'] # novi centar
                        if presek(linija, najbliza):
                            if najbliza.presla == False:
                                print("presao")
                                najbliza.presla = True                            
                                broj =  int(knn.predict(najbliza.slicica.reshape(1, 784)))
                                zbir += broj
                                print("broj: " + str(broj) + ", zbir: " + str(zbir))  
               
        else:
            break # ako nije ucitan frejm to je kraj snimka
    snimak.release()    

    cv.destroyAllWindows()
    return zbir



