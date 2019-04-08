import math

def presek_linija(linija1, linija2):
    xdiff = (linija1[0][0] - linija1[1][0], linija2[0][0] - linija2[1][0]) # x1 - x2 jedne linije i x1 - x2 druge linije
    ydiff = (linija1[0][1] - linija1[1][1], linija2[0][1] - linija2[1][1]) # isto samo za y1 - y2

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0] # formula determinante [1 1
                                                              #  0 2] 1*2 - 1*0

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('Linije se ne seku')

    d = (det(*linija1), det(*linija2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

# provera udaljenosti trenutne pozicije i preseka
def proveri_presek(trenutna_pozicija, presek):
    # odbacuju se pozicije ispod linije, detekcija se vrsi malo pre prolaska ispod linije, pa nam 
    # ove tacke ne trebaju 
    if trenutna_pozicija[1] > presek[1]:        
        #print('ispod')
        return False

    # euklidska udaljenost preseka i trenutne pozicije -  (x2-x1)**2 + (y2-y1)**2
    dist = math.sqrt( (trenutna_pozicija[0]-presek[0])**2 + (trenutna_pozicija[1]-presek[1])**2 )
    # ako je dovoljno blizu vrati da je ok
    if dist < 28 and dist > 11:
        return True

    # inace je predaleko
    #print('predaleko')
    return False

def presek(linija, kontura):
    # odbacuje se da se ne bi desio exception, ako su prva i zadnja tacke iste - to nije prava
    # ne moze se naci presek
    if kontura.poslednji_centar[0] == kontura.centar[0] and kontura.poslednji_centar[1] == kontura.centar[1]:
        #print('isti')
        return False

    # racuna presecnu tacku izmedju pravih
    x,y = presek_linija(linija, (kontura.centar, kontura.poslednji_centar)) # koordinate preseka

    # presek mora da se nalazi na duzi, ogranicimo po krajevima duzi
    if x < linija[0][0]: # ne sme biti pre prvog x-a
        #print('prelevo')
        return False
    if x > linija[1][0]: # ne sme biti posle zadnjeg x-a
        #print('predesno')
        return False
    
    # proveri udaljenost preseka i trenutne pozicije - da li je dovoljno blizu liniji
    return proveri_presek(kontura.poslednji_centar, (x,y))