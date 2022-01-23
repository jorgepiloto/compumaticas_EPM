# -*- coding: utf-8 -*-
# ---
# title: Noche estrellada con Python turtle
# author: Jorge Martínez Garrido
# date: 2022-01-28
# categories: ["Compumaticas"]
# tags: ["Python", "turtle"]
#
# jupytext:
#   encoding: '# -*- coding: utf-8 -*-'
#   text_representation:
#     extension: .md
#     format_name: md
# kernelspec:
#   display_name: Python 3
#   language: python
#   name: python3
# ---

# Una de las cosas que más me gustan es ver las estrellas por la noche. Un cielo
# de color negro lleno de pequeños puntos blancos me resulta algo precioso. ¿Y si
# dibujamos una noche estrellada con Python y turtle?
#
# Como siempre, el código fuente[^1] puedes encontrarlo al final del post.

# ## Atacando el problema
#
# Para visualizar mejor el problema, imaginemos un grupo de estrellas dispuestas en el cielo nocturno:
#
# ![Esquema noche estrellada](img/stars_background_auxiliary.png)
#
# A lo largo del tiempo, diversas culturas han agrupado las estrellas en formas conocidas bajo el nombre de constelaciones. En la imagen anterior se muestra la popular Osa Mayor. Nuestro objetivo es dibujar solamente las estrellas, no las líneas o las constelaciones.
#
# Para ello, lo que podemos hacer es:
#
# 1. Dibujar un fondo negro que simule el espacio sideral y la noche.
# 2. Generar puntos aleatorios con coordenadas x e y donde situar cada una de las estrellas.
# 3. Generar un radio aleatorio para cada estrella, lo que dará mayor realismo a la imagen.
#
# En este tutorial asumiremos que todas las estrellas son de color blanco, pero puedes animarte a darles otros colores como por ejemplo amarillo o azul.

import turtle


# ## Generando el fondo nocturno
#
# Vamos a crear una función que dibuje el cielo nocturno. Para ello nos bastará con pintar un rectángulo y rellenarlo de color negro. Solo hay un problema: turtle no sabe dibujar rectángulos. Debemos crear una función que dibuje estos elementos geométricos al igual que hicimos en el post [Dibujando el logo de los Juegos Olímpicos con Python turtle](https://jorgemartinez.space/posts/compumaticas/) para generar una circunferencia.
#
# Recordemos la goemetría de un rectángulo:
#
# ![Geometría de un rectángulo](img/rectangle_geometry.png)
#
# Podemos ver que si partimos de un origen de coordenadas centrado en $x$ e $y$, deberemos desplazarnos hasta el punto $(b/2, 0)$ para poder dibujar el rectángulo. Lo haremos en sentido anti-horario, es decir, al contrario de las manecillas del reloj. Debemos de recorrer los siguientes puntos:
#
# $$
# (b/2, 0) \rightarrow (b/2, a/2) \rightarrow (-b/2, a/2)  \rightarrow (-b/2, -a/2)  \rightarrow (b/2, -a/2) \rightarrow (b/2, 0) 
# $$
#
# donde $b$ es el tamaño de la base y $a$ la altura del rectángulo.
#
# La función para dibujar el cielo nocturno mediante un rectángulo se muestra a continuación:

def dibujar_cielo_nocturno(base, altura, color=(0, 0, 0)):
    """
    Dibuja un rectángulo de ancho y alto deseados que simula el cielo nocturno.
    
    Parameters
    ----------
    base: float
        Ancho del rectángulo para el cielo.
    altura: float
        Alto del rectángulo para el cielo.
    color: tuple
        Color del cielo, por defecto en negro.
    """
    
    # Podemos acortar los nombres para no repetir
    b_2, a_2 = base / 2, altura / 2
    
    # Calculamos las diferentes posiciones
    lista_puntos = [
        (b_2, a_2), (-b_2, a_2), (-b_2, -a_2), (b_2, -a_2), (b_2, 0)
    ]        
    
    # Levantar el lápiz para movernos al borde para empezar a dibujar
    turtle.penup()
    turtle.goto(b_2, 0)
    turtle.pendown()
    turtle.pencolor(color)
    
    # Pasamos por cada punto y rellenamos el rectángulo
    turtle.fillcolor(color)
    turtle.begin_fill()
    for (x, y) in lista_puntos:
        turtle.goto(x, y)
    turtle.end_fill()


# ## Generando las estrellas
#
# Una vez tenemos definida la rutina para crear el cielo nocturno es hora de crear una nueva que dibuje cierto número de estrellas sobre dicho fondo. Las estrellas deben de ser círculos blancos y el valor de sus radios oscila entre ciertos límites. Además, la posición de una estrella debe de ser aleatoria pero quedar enmarcada dentro del fondo creado anteriormente.

# Vamos a reutilizar la función `dibujar_anillo` del post [Dibujando el logo de los Juegos Olímpicos con Python turtle](https://jorgemartinez.space/posts/compumaticas/dibujando-el-logo-de-los-juegos-ol%C3%ADmpicos-con-python-turtle/). La llamaremos `dibujar_estrella` y la modificaremos para que en lugar de dibujar un anillo, dibuje un círculo relleno de color.

def dibujar_estrella(x, y, radio, color=(1, 1, 1)):
    """
    Dibuja un anillo dado su centro, radio, color RGB y grosor de línea.

    Parameters
    ----------
    x: float
        Coordenada horizontal para el centro de la estrella.
    y: float
        Coordenada vertical para el centro de la estrella.
    radio: float
        La longitud característica de la estrella, es decir, su radio.
    color: tuple
        Un tuple con los valores (r, g, b) para generar el color de la estrella.
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

    # Dibuja el círculo y lo rellena del color deseado
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.circle(radio)
    turtle.end_fill()

    # Levanta el lápiz y lo devuelve a la posición del centro del círculo
    turtle.penup()
    turtle.goto(x, y)


# Sabemos que podemos generar números aleatorios comprendidos entre $0$ y $1$. Podemos entender un valor en el rango $(0, 1)$ como un coeficiente $\eta$ que escala un determinado valor. Si $\eta=0$, entonces $\eta \cdot L = 0$. Por otro lado, si $\eta = 1$, entonces $\eta \cdot L = L$, lo que implica que para cualquier valor de $\eta$ entre $0$ y $1$ implica que el producto $\eta \cdot L$ tendrá un valor comprendido entre $0$ y $L$.
#
# Es importante darse cuenta de que el origen de coordenadas de turtle es el centro de la ventana y no la esquina de inferior izquierda de la misma. Por ello, debemos restar la mitad de la base y altura del rectángula a la hora de generar las coordenadas aleatorias de los puntos. 

from random import random


# Tras importar las funciones `random` para generar números aleatorios escribimos la función:

def dibujar_N_estrellas(N_estrellas, base, altura, radio_max=5):
    """
    Dibuja un número N de estrellas.
    
    Parameters
    ----------
    N_estrellas: int
        Número deseado de estrellas.
    base: float
        Ancho del rectángulo donde dibujar las estrellas.
    altura: float
        Alto del rectángulo donde dibujar las estrellas.
    radio_max: float
        Máximo radio posible para una estrella.
    """
    
    for i in range(N_estrellas):
        
        # Generamos valores aleatorios de x e y del ancho y el alto
        x_estrella = (random() - 0.5)* base
        y_extrella = (random() - 0.5)* altura
        
        # Genera un radio aleatorio
        radio_estrella = random() * radio_max

        # Dibujamos la estrella
        dibujar_estrella(x_estrella, y_extrella, radio_estrella)


# ## Dibujando la noche estrellada
#
# Una vez redactadas todas las funciones anteriores, es posible generar el siguiente código para conseguir dibujar nuestro fondo estrellado. Para lograr un mejor efector, vamos a esconder la "tortuga" utilizando `turtle.hideturtle()` y a darle la máxima velocidad posible aplicando `turtle.speed(0)`.

# +
# Escondemos la tortuga y le damos la máxima velocidad
turtle.hideturtle()
turtle.speed(0)

# Establecemos la resolución de pantalla (alto y ancho del rectángulo)
resolucion = (640, 480)

# Dibujamos el cielo nocturno y un total de 50 estrellas
dibujar_cielo_nocturno(*resolucion)
dibujar_N_estrellas(50, *resolucion)
turtle.mainloop()
# -

# ## Resultado
#
# Dado que estamos trabajando con números aleatorios, cada resultado será diferente salvo que fijemos la conocida como "semilla" o `seed`. De cualquier modo, ejecutando el código anterior deberías de obtener algo similar a la siguiente animación: 

# ![Resultado](img/stars_background.gif)

# ## Referencias
#
# [^1]: [Descargar el código fuente](https://github.com/jorgepiloto/compumaticas_EPM/blob/main/compumaticas_0/stars_background/main.py)
