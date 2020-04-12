import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-2s) %(message)s')


class Taller(object):
    def __init__(self, start=0):
        self.condicionMangasMAX = threading.Condition()
        self.condicionMangasMIN = threading.Condition()
        self.condicionCuerpoMAX = threading.Condition()
        self.condicionCuerpoMIN = threading.Condition()
        self.mangas = 0
        self.cuerpos = 0
        self.prenda = 0

    def incrementarManga(self):
        with self.condicionMangasMAX:
            if self.mangas >= 10:
                logging.debug("No hay espacio para mangas")
                self.condicionMangasMAX.wait()
            else:
                self.mangas += 1
                logging.debug("Manga creada, mangas=%s", self.mangas)
        with self.condicionMangasMIN:
            if self.mangas >= 2:
                logging.debug("Existen suficientes mangas")
                self.condicionMangasMIN.notify()

    def decrementarManga(self):
        with self.condicionMangasMIN:
            while not self.mangas >= 2:
                logging.debug("Esperando mangas")
                self.condicionMangasMIN.wait()
            self.mangas -= 2
            logging.debug("Mangas tomadas, mangas=%s", self.mangas)
        with self.condicionMangasMAX:
            logging.debug("Hay espacio para mangas")
            self.condicionMangasMAX.notify()

    def getMangas(self):
        return (self.mangas)

    def incrementarCuerpo(self):
        with self.condicionCuerpoMAX:
            if self.cuerpos >= 10:
                logging.debug("No hay espacio para cuerpos")
                self.condicionCuerpoMAX.wait()
            else:
                self.cuerpos += 1
                logging.debug("Cuerpo creado, cuerpo=%s", self.cuerpos)
        with self.condicionCuerpoMIN:
            if self.cuerpos >= 1:
                logging.debug("Existen suficientes cuerpos")
                self.condicionCuerpoMIN.notify()

    def decrementarCuerpo(self):
        with self.condicionCuerpoMIN:
            while not self.cuerpos >= 1:
                logging.debug("Esperando cuerpo")
                self.condicionCuerpoMIN.wait()
            self.cuerpos -= 1
            logging.debug("Cuerpo tomado, cuerpos=%s", self.cuerpos)
        with self.condicionCuerpoMAX:
            logging.debug("Hay espacio para cuerpos")
            self.condicionCuerpoMAX.notify()

    def getCuerpos(self):
        return (self.cuerpos)

    def incrementarPrenda(self):
        self.prenda += 1

    def getPrendas(self):
        return (self.prenda)


def crearManga(Taller):
    while (Taller.getMangas() <= 10):
        Taller.incrementarManga()
        time.sleep(5)


def crearCuerpo(Taller):
    while (Taller.getCuerpos() <= 10):
        Taller.incrementarCuerpo()
        time.sleep(5)


def ensamblaPrenda(Taller):
    logging.debug('Ensamblando todo')
    while (Taller.getPrendas() <= 10):
        logging.debug("Tomando materiales")
        Taller.decrementarManga()
        Taller.decrementarCuerpo()
        Taller.incrementarPrenda()
        logging.debug("Prenda hecha, prendas=%s", Taller.getPrendas())
        time.sleep(10)


taller = Taller()
Lupita = threading.Thread(name='Lupita(mangas)', target=crearManga, args=(taller,))
Sofia = threading.Thread(name='Sofía(cuerpos)', target=crearCuerpo, args=(taller,))
persona3 = threading.Thread(name='persona(ensamble)', target=ensamblaPrenda, args=(taller,))
Lupita.start()
Sofia.start()
persona3.start()
Lupita.join()
Sofia.join()
persona3.join()
