# wordle-bot

El programa se ejecuta desde wordle_bot.py, donde se lanza Selenium y se cogen las referencias a los elementos de la página web de Wordle con los que será necesario interaccionar. En la clase Partida de este mismo fichero se debe indicar la ruta en la que se encuentran los drivers de Selenium (geckodriver para Firefox y chromedriver para Chrome). Por defecto se ha utilizado Firefox.

La clase Palabra hace de capa intermediaria entre Partida (el más alto nivel) y GestorPalabras, que contiene la lógica relacionada con la selección de las palabras adecuadas para cada ronda.

La clase Diccionario gestiona la entrada y salida con el S.O. para leer y escribir ficheros de palabras.

Aunque el proyecto se ha desarrollado y probado en el wordle en español (https://wordle.danielfrg.com/) está pensado para poder usarse con cualquier lengua.


