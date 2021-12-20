# Titulo: Dibujando el logo de los Juegos Olímpicos con Python turtle
# Autor: Jorge Martínez Garrido
# 
# Vamos a ver cómo podemos dibujar el logo de los Juegos Olímpicos con Python
# turtle. Sin embargo vamos a añadir una condición: el logo debe de estar
# proporcionado al radio de los anillos que lo forman.
#
# Como siempre, el código fuente[^1] puedes encontrarlo al final del post.

# ## Atacando el problema
#
# El logo de los Juegos Olímpicos consta de un total de cinco circunferencias o
# anillos dispuestoss en dos filas: tres arriba y dos abajo.
#
# ![Logo de los Juegos Olímpicos](img/logo.png)
#
# Nótese que existe cierto espacio entre los anillos. Además, los anillos de abajo
# resultan estar posicionados justo en la vertical de los centros de los anillos
# superiores. Aprovecharemos este hecho para poder dibujar el logo.
#
# A continuación se muestra el logo junto con líneas auxiliares para visualizar
# mejor la geometría que existe detrás del logo.
#
# ![Logo con líneas auxiliares](img/logo_auxiliary.png)
#
# Para dibujar el logo anterior podemos seguir los siguientes pasos:
#
# 1. Crear una función que nos permita pintar una circunferencia en un lugar del
#    planos dado su centro, radio y el color.
#
# 2. Calcular las posiciones para cada uno de los centros de los anillos que
#    forman el logo.
#
# 3. Utilizar un bucle para llamar a la función que dibuja los anillos un total de
#    5 veces y que pinte en cada iteración cada uno de los anillos.

import turtle

# ## Creando la función para dibujar un anillo
#
# En turtle existe una función llamada `circle`, la cual permite dibujar un
# círculo dado su radio. El problema es que turtle lo dibuja como si fuera un
# compás, por lo que tenemos que "mover" el centro proporcionado por el usuario a
# cualquier punto del anillo. Un punto sencillo es el que está localizado al
# norte, es decir, en la parte superior del anillo. La imagen que sigue describe
# la geometría del anillo:
#
# ![Geometría de un anillo](img/anillo.png)
#
# Así pues, las coordenadas del centro $p_c$ y las del punto norte $p_N$ serán:
#
# $$
# p_c = [x, y]\quad\quad
# p_N = [x, y + R]
# $$
#
# Teniendo en cuenta la geometría anterior es posible implementar la siguiente
# función en Python:


def dibujar_anillo(x, y, radio, color=(0, 0, 0), grosor=2.5):
    """
    Dibuja un anillo dado su centro, radio, color RGB y grosor de línea.

    Parameters
    ----------
    x: float
        Coordenada horizontal para el centro del anillo.
    y: float
        Coordenada vertical para el centro del anillo.
    radio: float
        La longitud característica del anillo, es decir, su radio.
    color: tuple
        Un tuple con los valores (r, g, b) para generar el color del anillo.
    grosor: float
        Un valor numérico para indicar el grosor de la línea del anillo.
    """

    # Levanta el lápiz para no crear líneas no deseadas
    turtle.penup()

    # Turtle dibuja una circunferencia desde uno de sus puntos. Por eso
    # calculamos el punto más al norte de la de circunferencia.
    x_norte, y_norte = x, y + radio

    # Mueve el lápiz a la parte de arriba del círculo, lo apunta a la izquierda,
    # fija el color y su tamaño de línea
    turtle.goto(x_norte, y_norte)
    turtle.setheading(180)
    turtle.pencolor(color)
    turtle.pensize(grosor)

    # Dibuja el círculo
    turtle.pendown()
    turtle.circle(radio)

    # Levanta el lápiz y lo devuelve a la posición del centro del círculo
    turtle.penup()
    turtle.goto(x, y)


# ## Calculando los centros
#
# Para calcular la posición de los círculos, es necesario conocer el valor del
# radio. Por ello, al describir el problema hemos dicho que todo el dibujo debe de
# estar escalado al radio: cambiar su valor cambia la posición de los centros en
# el dibujo. Además, para radios de gran valor, mayor grosor de línea en los
# anillos.
#
# Podemos comenzar definiendo el espacio que existe entre dos anillos. Si nos
# fijamos en la segunda imagen de este post (la que tiene las líneas auxiliares en
# el logo), podemos decir que el espacio es más o menos un cuarto del radio de los
# anillos. Llamaremos el grosor $\Delta x = R / 4$. Así pues, la distancia entre
# los centros de dos anillos resulta ser:
#
# $$
# d_x = R + \Delta x + R = 2R + \Delta x
# $$
#
# Para la distancia vertical entre dos centros, podemos ver que:
#
# $$
# d_y = R + \Delta x
# $$
#
# Para calcular a qué distancia se encuentran los centros superiores e inferiores
# con respecto a la línea horizontal de referencia, podemos calcular por
# geometría:
#
# $$
# l_1 = d_y / 2\quad\quad
# l_2 = -d_y / 2
# $$

# Conocido todo lo anterior es posible generar el siguiente código:
#


def generar_centros(radio):
    """
    Devuelve las coordenadas para cada uno de los centros de los anillos.

    Parameters
    ----------
    radio: float
        Radio de los anillos. Se utiliza para escalar todo el dibujo.

    Returns
    -------
    lista_centros: list
        Lista con tuplas conteniendo las coordenadas x e y de los centros.
    """

    # Calculamos la separación entre dos anillos
    delta_x = radio / 4

    # Resolvemos la distancia horizontal y vertical entre dos centros
    d_x = 2 * radio + delta_x
    d_y = radio + delta_x

    # Declaramos la lista que contendrá los centros
    lista_centros = []

    # Resolvemos los centros teniendo en cuenta en qué fila estamos
    for i in range(6):
        x_centro = d_x * (i - 1) if i < 3 else d_x * (i - 3.5)
        y_centro = d_y / 2 if i < 3 else -d_y / 2
        centro = (x_centro, y_centro)
        lista_centros.append(centro)

    return lista_centros


# ## Dibujando cada uno de los anillos
#
# Una vez definidas todas las funciones anteriores, lo único que nos queda por
# hacer es llamarlas en el orden correcto y utilizar un bucle para pintar cada uno
# de los anillos. Pero antes, vamos a declarar dentro de una lista los colores que
# vamos a utilizar:

colores = ["blue", "black", "red", "yellow", "green"]

# Ahora, definimos el radio deseado y generamos los círculos:

radio = 150
lista_centros = generar_centros(radio)

# Utilizamos un bucle para pintar los cinco anillos:

for (x_centro, y_centro), color in zip(lista_centros, colores):
    dibujar_anillo(x_centro, y_centro, radio, color, grosor=radio * 0.1)
turtle.mainloop()

# ## Resultado
#
# Ejecutando todos los códigos anteriores es posible obtener el siguiente resultado:
#
# ![Logo animado](img/logo_animation.gif)
#
# Prueba a cambiar el valor del radio y podrás comprobar como el dibujo cambia en
# proporción a dicho radio.
