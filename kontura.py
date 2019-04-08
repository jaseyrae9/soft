import copy

class Kontura:

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def presla(self):
        return self.__presla

    @presla.setter
    def presla(self, presla):
        self.__presla = presla

    @property
    def centar(self):
        return self.__centar

    @centar.setter
    def centar(self, centar):
        self.__centar = centar

    @property
    def poslednji_centar(self):
        return self.__poslednji_centar

    @poslednji_centar.setter
    def poslednji_centar(self, poslednji_centar): 
        self.__poslednji_centar = poslednji_centar

    @property
    def slicica(self):
        return self.__slicica

    @slicica.setter
    def slicica(self, slicica):
        self.__slicica = slicica

    def __init__(self, id, presla, centar, slicica): 
        self.__id = id
        self.__presla = presla
        self.__centar = copy.deepcopy(centar)
        self.__poslednji_centar = centar
        self.__slicica = slicica
