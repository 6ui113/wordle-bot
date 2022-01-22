from gestor_palabras import GestorPalabras


class Palabra:

    letras: list[chr]
    opciones: list[list[chr]]
    letras_contenidas: list[chr]
    posible_palabra: str
    gp: GestorPalabras
    num_ronda: int

    def __init__(self, n_letras):
        print('Creando objeto Palabra de {} letras...'.format(n_letras))
        self.gp = GestorPalabras(n_letras)
        self.num_ronda = 0

    def procesa_respuesta(self, respuesta) -> bool:
        """
        Recibe como parámetro una lista de str como esta:
        ['ausente', 'presente', 'presente', 'correcta', 'ausente']
        donde se indica en cada posición si la letra probada es correcta, está presente o ausente del resultado.

        Hace las modificaciones pertinentes en la lista de posibles letras de cada posición.
        Devuelve True una vez realizadas.
        """
        i = 0
        for posicion in self.gp.char_freq:

            if respuesta[i] == 'ausente':
                self.gp.incorrect_chars.append(self.posible_palabra[i])
                # Elimina esa letra de todas las posiciones
                for pos in self.gp.char_freq:
                    try:
                        if len(pos) > 1:
                            # Si queda más de una posible letra en esta posición:
                            pos.pop(self.posible_palabra[i])

                    except KeyError as e:
                        # Ya borrada
                        pass

            elif respuesta[i] == 'correcta':
                # Deja la letra aceptada como única opción en esa posición
                self.gp.char_freq[i] = {self.posible_palabra[i]: 1}
                self.gp.guessed[i] = True

                # Añade la letra a las letras contenidas en la palabra si no estaba ya
                if self.posible_palabra[i] not in self.gp.present_chars:
                    self.gp.present_chars.append(self.posible_palabra[i])

            elif respuesta[i] == 'presente':
                # Elimina la letra de la posición actual
                try:
                    self.gp.char_freq[i].pop(self.posible_palabra[i])
                except KeyError as e:
                    # Ya se había eliminado
                    pass

                # Añade la letra a las letras contenidas en la palabra
                self.gp.present_chars.append(self.posible_palabra[i])

            i += 1

        self.gp.recalculate_ratios()

        print('CHAR FREQUENCY RESTANTE PARA CADA POSICIÓN: ')
        for elem in self.gp.char_freq:
            print(elem)

        return True

    def siguiente_palabra(self):
        self.posible_palabra = self.gp.choose_word()
        self.gp.num_round = self.num_ronda
        return self.posible_palabra

