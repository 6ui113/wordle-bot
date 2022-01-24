class Diccionario:
    """
    Gestiona la interacción del programa con el sistema operativo en la lectura y escritura de ficheros de palabras.
    """

    PATH_DICTIONARY = "es_dictionary.txt"
    SELECTED_WORDS = "selected_words"

    accent_chars = {
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U',
        'Ü': 'U',
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'ü': 'u'
    }

    @classmethod
    def remove_char_accent(cls, char):
        """
        Cambia una letra con tilde o diéresis por la misma letra limpia y la devuelve.
        """
        if char in cls.accent_chars:
            char = cls.accent_chars[char]
        return char

    @classmethod
    def remove_word_accents(cls, word):
        """
        Elimina tildes y diéresis de una palabra completa y la devuelve.
        """
        new_word = ''
        for c in word:
            new_word += cls.remove_char_accent(c)
        return new_word

    @classmethod
    def extract_words(cls, num_chars, encoding='utf-8'):
        """
        Lee cada línea de un fichero de entrada y si la longitud de la línea leída corresponde
        con el número de caracteres especificado en [num_chars], escribe la línea en el fichero de salida.

        Elimina tildes y diéresis y escribe las palabras en mayúsculas.

        Por ejemplo, sirve para extraer todas las palabras de 5 letras de un fichero con palabra por línea.
        """
        path_out = cls.SELECTED_WORDS + '_' + str(num_chars) + '_chars'
        with open(cls.PATH_DICTIONARY, 'r', encoding=encoding) as f_in:
            with open(path_out, 'w', encoding=encoding) as f_out:
                while True:
                    line = f_in.readline()
                    if line == '':
                        break
                    if len(line.strip('\n')) == num_chars:
                        f_out.write(cls.remove_word_accents(line.upper()))

    @classmethod
    def sort_dict(cls, dict_in: dict, reverse=True) -> dict:
        """
        Ordena el diccionario recibido como entrada en base al valor de cada elemento.
        Por defecto ordena de mayor a menor.
        """
        aux: list
        sorted_dict = {}

        # Creamos una lista con las claves ordenadas en base a los valores
        aux = sorted(dict_in, key=dict_in.get, reverse=reverse)
        for key in aux:
            sorted_dict[key] = dict_in[key]

        return sorted_dict

    @classmethod
    def dict_ratios(cls, dict_in):
        """
        Dado un diccionario de entrada cuyos valores son numéricos, calcula para cada uno qué ratio ocupa de la
        suma total de valores y lo sustituye su valor.

        Ejemplo de entrada: {'a': 700, 'o': 180, 'r': 120}
        Ejemplo de salida: {'a': 0.70, 'o': 0.18, 'r': 0.12}
        """
        total = 0
        for key in dict_in:
            total += dict_in[key]
        for key in dict_in:
            dict_in[key] /= total
        return dict_in

    @classmethod
    def char_frequency(cls, num_chars, encoding='utf-8'):
        """
        Para un fichero de entrada dado [f_in] cuenta el número de ocurrencias de cada caracter en cada posición y en
        base al porcentaje de veces que aparece le da un peso entre 0 y 1.

        Devuelve una lista de diccionarios donde cada diccionario contiene el peso de cada caracter para esa posición.

        Se da por hecho que en el fichero leído las palabras no llevan tilde y están normalizadas a mayúsculas o
        minúsculas. En caso de que no las estadísticas que saca no son fiables..

        Ejemplo de salida:
        [{'a': 0.70, 'o': 0.18, 'r': 0.12}, {'e': 0.50, 'i': 0.50}]
        """
        char_freq = []
        f_in = cls.SELECTED_WORDS + '_' + str(num_chars) + '_chars'
        for n in range(num_chars):
            char_freq.append({})

        with open(f_in, 'r', encoding=encoding) as f:
            while True:
                linea = f.readline().strip('\n')  # Molaría hacerlo con expresiones regulares?

                if linea == '':
                    break  # Final de fichero

                i = 0
                for c in linea:
                    try:
                        char_freq[i][c] += 1
                    except KeyError as e:
                        char_freq[i][c] = 1
                    finally:
                        i += 1

        for i in range(len(char_freq)):
            char_freq[i] = Diccionario.sort_dict(char_freq[i])

        for position in char_freq:
            position = cls.dict_ratios(position)
        return char_freq

    @classmethod
    def get_words(cls, num_chars, encoding='utf-8'):
        """
        Para un número de caracteres dado, devuelve una lista de palabras leídas del diccionario de la lengua que se
        esté usando.

        Si el fichero con las palabras de [num_chars] letras no existe, lo crea, analizando el diccionario por defecto
        que se haya establecido en la contante [PATH_DICTIONARY].
        """
        path_in = cls.SELECTED_WORDS + '_' + str(num_chars) + '_chars'
        words = []
        try:
            with open(path_in, 'r', encoding=encoding) as f:
                while True:
                    line = f.readline().strip('\n')
                    if line == '':
                        break
                    words.append(line.upper())
        except FileNotFoundError as e:
            cls.extract_words(num_chars)
            words = cls.get_words(num_chars)
        return words
