import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from palabra import Palabra


class Partida:

    n_rondas: int
    n_letras: int
    palabra: Palabra
    n_ronda: int

    def __init__(self, url):
        os.environ['PATH'] += 'C:/SeleniumDrivers'

        self.driver = webdriver.Firefox()
        self.driver.get(url)
        self.driver.set_window_size(480, 720)

        self.pantalla_bienvenida()
        self.wordle = self.get_wordle()
        self.tecla = self.get_teclado()
        self.palabra = Palabra(self.n_letras)
        self.n_ronda = 0

    def pantalla_bienvenida(self):
        # Si sale la pantalla de bienvenida le da al botón de jugar
        try:
            elem = self.driver.find_element(By.XPATH, "//*[text()='Jugar!']")
            elem.click()
        except NoSuchElementException as e:
            pass

    def get_wordle(self):
        wordle = []
        # Localiza la rejilla y coge las referencias a cada línea en una lista de WebElements
        filas = self.driver.find_elements(By.CSS_SELECTOR, "div.grid.grid-cols-5.gap-1.w-full")
        for elem in filas:
            # Cogemos una referencia a cada cuadro dentro de cada fila
            wordle.append(elem.find_elements(
                By.CSS_SELECTOR,
                "div.w-full.h-full.inline-flex.justify-center.items-center.text-white"
            ))

        print('Localizadas referencias a {} filas con {} casillas en cada fila'.format(len(wordle), len(wordle[0])))
        self.n_rondas = len(wordle)
        self.n_letras = len(wordle[0])

        return wordle

    def get_teclado(self):
        teclado = self.driver.find_elements(By.CSS_SELECTOR, "div.flex.gap-1")
        tecla = {}
        for fila in teclado:
            teclas = fila.find_elements(By.TAG_NAME, 'button')
            for t in teclas:
                tecla[t.text] = t
        return tecla

    def escribe_palabra(self, palabra_a_escribir: str):
        for c in palabra_a_escribir:
            self.tecla[c].click()
        else:
            self.tecla['ENTER'].click()

    def lee_respuesta(self, n_ronda: int):
        resultado = []
        for casilla in self.wordle[n_ronda]:
            clases = casilla.get_attribute("class")

            if 'bg-correct' in clases:
                # Letra correcta
                resultado.append('correcta')
            elif 'bg-present' in clases:
                # Letra presente
                resultado.append('presente')
            else:
                # Letra no presente
                resultado.append('ausente')

        return resultado

    def ronda(self):
        print("\n\n\n{}".format('-' * 30))
        print("RONDA {}.".format(self.n_ronda + 1))

        self.escribe_palabra(self.palabra.siguiente_palabra().upper())

        print("\n\nProbando palabra: {}".format(self.palabra.posible_palabra))
        time.sleep(1)

        respuesta = self.lee_respuesta(self.n_ronda)
        print(respuesta)
        if respuesta == ['correcta', 'correcta', 'correcta', 'correcta', 'correcta']:
            return True
        self.palabra.procesa_respuesta(respuesta)
        time.sleep(1)
        self.n_ronda += 1
        self.palabra.num_ronda = self.n_ronda

        return False

    def start(self):
        for num_round in range(self.n_rondas):
            if partida.ronda():
                print('Ha ganado el bot!')
                break  # Se gana la partida antes de la última ronda.


if __name__ == '__main__':
    partida = Partida("https://wordle.danielfrg.com/")
    partida.start()

