# Diego Sahid Garcia Galvan
# Created on 16/02/2023

from pygame import *
import sys
import math

# formula de la trayectoria de un proyectil: https://www.fisicalab.com/apartado/lanzamiento-horizontal

# Funcion para obtener el alcance maximo del proyectil en base a la velocidad inicial en x y el tiempo de vuelo
def AlcanceMaximo(velocity, gravity, height):
    tiempo = math.sqrt((2*height)/gravity)
    alcance_maximo = velocity*tiempo
    return alcance_maximo

# Funcion para obtener el desplazamiento en y en base a el desplazamiento en x
def CalculaY(velocity, gravity, height, x, y):
    for i in x:
        numerador = round(gravity*((i)**2), 2)
        denominador = round(2*(velocity**2))
        y.append(height-(numerador/denominador))

# Funcion para pintar el camino del proyectil
def DibujarCamino(points):
    for p in points:
        draw.circle(screen, (102,102,255), (p[0], screen_height - p[1]), 5, 0)

# Funcion para calcular la velocidad por teorema de Torricelli
def CalculaVelocidad(gravity, height):
    velocity = math.sqrt(2*gravity*height)
    return velocity

# def DrawGraph(x, y):
#     plt.plot(x, y)
#     plt.xlabel("x coordinate")
#     plt.ylabel("y coordinate")
#     plt.title("Proyectil")
#     plt.show()


screen_width = 800
screen_height = 600
FPS = 100

# Condiciones iniciales de los lanzamientos
altura_liquido0 = 32
altura_liquido1 = 16
altura_liquido2 = 4
gravedad = 9.8
velocidad0 = CalculaVelocidad(gravedad, altura_liquido0)
velocidad1 = CalculaVelocidad(gravedad, altura_liquido1)
velocidad2 = CalculaVelocidad(gravedad, altura_liquido2)
shooting = False

# Coordenadas desde las que iniciara el recorrido
x_pantalla = 250
y_pantalla = 155
xCoord = 0
yCoord = 0

# Defino mi alcance maximo como una variable
alcance_maximo = int(AlcanceMaximo(velocidad0, gravedad, altura_liquido0))

# Creo el vector x desde 0 hasta el alcance maximo
eje_x0 = [i for i in range(screen_width)]
eje_x1 = [i for i in range(screen_width)]
eje_x2 = [i for i in range(screen_width)]

# Inicializo mi vector y vacio
eje_y0 = []
eje_y1 = []
eje_y2 = []

# Lista de puntos que tiene el camino del proyectil
puntos0 = []
puntos1 = []
puntos2 = []

# Llamo a la funcion que llenara el vector y
CalculaY(velocidad0, gravedad, altura_liquido0, eje_x0, eje_y0)
CalculaY(velocidad1, gravedad, altura_liquido1, eje_x1, eje_y1)
CalculaY(velocidad2, gravedad, altura_liquido2, eje_x2, eje_y2)

# print(eje_y0)
# print(eje_y1)
# print(eje_y2)

heightScreen = 600
widthScreen = 800

init()
screen = display.set_mode((widthScreen,heightScreen))

clock = time.Clock()

widthAgua, heightAgua = 150, 300
widthContenedor, heightContenedor = 160, 310
yAgua = ((heightScreen/2)-(heightAgua/2)) # Almaceno la posicion en y del agua en una 
                                          # variable para poder modificarla con facilidad
fontS = font.SysFont('RockWell', 30)
fontB = font.SysFont('RockWell', 45)

contenedor = Rect((95,(heightScreen//2)-(heightContenedor//2),widthContenedor,heightContenedor))

mesa = transform.scale(image.load('ExperimentacionFisica/mesa.png'), (300,200))

# Datos numericos que se despliegan como texto
titulo = fontB.render('Simulación del vaciado de una botella', True, (102,102,255))
dato0 = fontS.render('Velocidad a ' + str(altura_liquido2) + 'cm: ' + str(round(math.sqrt(2*altura_liquido2/100*gravedad), 2)) + 'm/s', True, (0,0,0))
dato1 = fontS.render('Velocidad a ' + str(altura_liquido1) + 'cm: ' + str(round(math.sqrt(2*altura_liquido1/100*gravedad), 2)) + 'm/s', True, (0,0,0))
dato2 = fontS.render('Velocidad a ' + str(altura_liquido0) + 'cm: ' + str(round(math.sqrt(2*altura_liquido0/100*gravedad), 2)) + 'm/s', True, (0,0,0))

while True:
    agua = Rect((100,yAgua,widthAgua, heightAgua))
    tick = clock.tick(FPS)/1000
    screen.fill((224,224,224))
    # Llamo a la funcion que pintara todos los puntos del camino del proyectil
    for e in event.get():
        if e.type == QUIT: sys.exit()
        if e.type == KEYDOWN:
            # Asi controlo cuando inicia la animacion
            if e.key == K_SPACE and shooting == False:
                shooting = True
            elif e.key == K_SPACE and shooting == True:
                shooting = False
    # Una vez inicia la animacion dibujo pequenios circulos con su centro en las coordenadas x y y que calculamos anteriormente
    if shooting:
        if (len(eje_x0) > 1 and len(eje_y0) > 1):
            # Voy agregando las coordenadas recorridas a la lista del camino del proyectil
            if eje_y0[0] >= -155:
                puntos0.append((eje_x0[0]+x_pantalla, eje_y0[0]+y_pantalla))
                puntos1.append((eje_x1[0]+x_pantalla, eje_y1[0]+y_pantalla+150))
                puntos2.append((eje_x2[0]+x_pantalla, eje_y2[0]+y_pantalla+250))
                eje_x0.pop(0)
                eje_x1.pop(0)
                eje_x2.pop(0)
                eje_y0.pop(0)
                eje_y1.pop(0)
                eje_y2.pop(0)
        heightAgua -= 0.3
        yAgua += 0.3
    # heightAgua -= 50
    # yAgua += 50
    # if heightAgua == 50:
    #     heightAgua = 300
    #     yAgua = ((heightScreen/2)-(heightAgua/2))
    draw.rect(screen, (64,64,64), contenedor)
    # Pinta el chorro de agua solo si la altura del liquido es mayor a la de el orificio de salida
    if heightAgua >= 0:
        if heightAgua > 258:
            DibujarCamino(puntos2)
        if heightAgua > 167:
            DibujarCamino(puntos1)
        if heightAgua > 32:
            DibujarCamino(puntos0)
    draw.rect(screen, (102,102,255), agua,) # (102,102,255)
    screen.blit(mesa, (25,455))
    # Despliego los textos
    screen.blit(titulo, ((widthScreen//2)-(titulo.get_width()//2),40))
    screen.blit(dato0, ((widthScreen//4)*2.9-(dato0.get_width()//2),(heightScreen//4)*1-(dato0.get_height()//2)))
    screen.blit(dato1, ((widthScreen//4)*2.9-(dato1.get_width()//2),(heightScreen//4)*2-(dato1.get_height()//2)))
    screen.blit(dato2, ((widthScreen//4)*2.9-(dato2.get_width()//2),(heightScreen//4)*3-(dato2.get_height()//2)))
    display.flip()

pygame.quit()