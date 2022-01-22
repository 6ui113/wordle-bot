from diccionario import Diccionario


class GestorPalabras:
    """
    Interacciona entre la clase Diccionario y la clase Palabra. Contiene las herramientas para puntuar cada palabra
    en base a las estadísticas obtenidas en Diccionario y las respuestas que se van obteniendo del wordle, así como
    para eliminar las palabras que no están presentes en la solución.
    """

    num_chars: int
    words: list[str]
    char_freq: list[dict] # La clave de cada dict es un char y el valor un flotante de 0 a 1 que indica su peso.
    present_chars: list[chr]
    incorrect_chars: list[chr]
    guessed: list[bool]
    num_guessed: int
    num_round: int

    def __init__(self, num_chars):
        print('Creando GestorPalabras...')
        self.num_chars = num_chars
        self.words = Diccionario.get_words(num_chars)
        self.char_freq = Diccionario.char_frequency(num_chars)
        self.present_chars = []
        self.incorrect_chars = []
        self.guessed = [False, False, False, False, False]
        self.num_guessed = 0
        self.num_round = 0

    def recalculate_ratios(self):
        for elem in self.char_freq:
            elem = Diccionario.dict_ratios(elem)

    def rank_word(self, word):
        """
        PRE:
        [word] es un string que contiene una palabra
        [present_chars] es una lista de caracteres que obligatoriamente pertenecen a la palabra.

        POST:
        Para cada caracter perteneciente a [word], se lee el peso de ese caracter en el diccionario [char_freq] para
        esa posición en específico y se suma a la variable [rank] para establecer una puntuación.
        Devuelve el valor de [rank]
        """
        rank = 0
        i = 0
        for c in word.upper():
            try:
                # Calcula la puntuación sumando los ratios de cada letra en cada posición
                rank += self.char_freq[i][c]
                # Además si contiene letras que seguro están presentes, gana puntuación extra de manera proporcional
                # al número de huecos restantes
                if c in self.present_chars:
                    rank += self.num_guessed / self.num_chars
            except KeyError as e:
                pass
            i += 1
        return rank

    def rank_words(self):
        aux_dict = {}
        aux_keys = []
        for word in self.words:
            aux_dict[word] = self.rank_word(word)

        if self.num_round == 0:
            # Si es la primera ronda premia a las palabras con más caracteres diferentes entre sí
            for key in aux_dict:
                aux_dict[key] *= len(set(key))

        aux_dict = Diccionario.sort_dict(aux_dict)

        pp = 0
        for elem in aux_dict:
            if pp >= 100:
                break
            print(f'{elem}: {aux_dict[elem]}', end=', ')
            pp += 1

        return [key for key, value in aux_dict.items()]

    def filter_by_correct_chars(self):
        aux_list = self.words.copy()

        for word in aux_list:
            for position in self.char_freq:
                if len(position) == 1:
                    for elem in position:
                        if elem not in word:
                            try:
                                aux_list.remove(word)
                            except ValueError:
                                # Ya se había eliminado
                                pass

        return aux_list

    def filter_by_present_chars(self):
        aux_list = self.words.copy()

        # Descartamos palabras que no contengan los caracteres que se sabe que están presentes
        if self.present_chars:
            for c in self.present_chars:
                new_list = []
                for word in aux_list:
                    if c in word:
                        new_list.append(word)
                aux_list = new_list.copy()

        return aux_list

    def filter_by_incorrect_chars(self):
        aux_list = self.words.copy()

        # Descartamos palabras que contienen caracteres incorrectos
        if self.incorrect_chars:
            for c in self.incorrect_chars:
                for word in aux_list:
                    if c in word and c not in self.present_chars:
                        aux_list.remove(word)

        return aux_list

    def calculate_guessed(self):
        n = 0
        for elem in self.guessed:
            if elem:
                n += 1
        return n

    def choose_word(self):
        """
        Se descartan todas las palabras que no contengan los caracteres especificados en [present_chars]
        """
        self.num_guessed = self.calculate_guessed()
        print('Letras adivinadas: {}. Caracteres presentes: {}'.format(self.num_guessed, self.present_chars))

        self.words = self.filter_by_correct_chars()
        self.words = self.filter_by_present_chars()
        self.words = self.filter_by_incorrect_chars()

        self.words = self.rank_words()
        print("\n\nEligiendo entre {} posibles palabras...".format(len(self.words)))
        print(self.words[:20], ' ...')
        return self.words[0]

