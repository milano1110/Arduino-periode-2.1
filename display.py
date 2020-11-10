# install pg: python -m pip install pg==2.0.0
#importeer benodigde modules en libraries
import pygame as pg
import time
import random
import math
import numpy
import matplotlib.pyplot as mpl
import serial
from pygame_widgets import Slider, TextBox

#with serial.Serial('COM5', 9600) as ser:
#    x = ser.readline()
#    print(x)

#    ser.close()
# resolutie
canvasWidth = 800
canvasHeight = 400
# kleuren
color_dark = (250,250,250)
color_light = (150,150,150)
color_red = (255,0,0)
color_redDark = (150,0,0)
color_green = (0,255,0)
color_greenDark = (0,150,0)
# driehoekige knoppen voor scherm omhoog en scherm omlaag
info_knop1Triangle_omhoog = [(canvasWidth/2-50,canvasHeight/4),(canvasWidth/2+50,canvasHeight/4),(canvasWidth/2, canvasHeight/4-50)]
info_knop1Triangle_omlaag = [(canvasWidth/2-50,canvasHeight - canvasHeight/4),(canvasWidth/2+50,canvasHeight - canvasHeight/4),(canvasWidth/2,canvasHeight - canvasHeight/8)]

autoButton1 = [(canvasWidth/2, canvasHeight/2), 50]
#info_graph_temp = [canvasWidth/16, canvasWidth/4, canvasHeight/8, 0, 250, 300]
#info_graph_light = [canvasWidth - canvasWidth/2 + canvasWidth/8, canvasWidth/16, canvasHeight/8, 0, 250, 300]
# knoppen voor grafieken voor temperatuur en licht
graph_temp1 = pg.Rect(canvasWidth/2-50, canvasWidth/4+55, canvasHeight/8+50, canvasHeight/8 - 10)
graph_light1 = pg.Rect(canvasWidth/2-50, canvasWidth/4-95, canvasHeight/8+50, canvasHeight/8 - 10)


#def detectClickRectangle(rect ,mouse):
#    if rect[0] <= mouse[0] <= rect[1] and rect[2] <= mouse[1] <= rect[3]:
#        return True
#    else:
#        return False

# klik detectie voor cirkels
def detectMouseInCircle(center, radius, mouse):
    if radius >= math.sqrt(math.pow(mouse[0] - center[0], 2) + math.pow(mouse[1] - center[1], 2)):
        return True
    else:
        return False
# klik detectie voor driehoeken
def detectMouseInTriangle(triangle, mouse):
    det = (triangle[1][0] - triangle[0][0]) * (triangle[2][1] - triangle[0][1]) - (triangle[1][1] - triangle[0][1]) * (triangle[2][0] - triangle[0][0])

    if (det * ((triangle[1][0] - triangle[0][0]) * (mouse[1] - triangle[0][1]) - (triangle[1][1] - triangle[0][1]) * (mouse[0] - triangle[0][0])) > 0) == True and (det * ((triangle[2][0] - triangle[1][0]) * (mouse[1] - triangle[1][1]) - (triangle[2][1] - triangle[1][1]) * (mouse[0] - triangle[1][0])) > 0) == True and (det * ((triangle[0][0] - triangle[2][0]) * (mouse[1] - triangle[2][1]) - (triangle[0][1] - triangle[2][1]) * (mouse[0] - triangle[2][0])) > 0) == True:
        return True
    else:
        return False

def main():
    auto1 = True
    color_up_1 = color_red
    color_up_2 = color_red
    array_temp1 = []
    array_light1 = []
    sunscreen1 = False
    w = None
    a = 0
    t = 0
    intensity = 0
    maxAfstand = 160
    isUitgerold = False
    ser = serial.Serial('COM4', 9600)  # Opent poort 9600 op COM4
    ser2 = serial.Serial('COM3', 9600)  # Opent poort 9600 op COM3
    pg.init()
    pg.font.init()
    font = pg.font.SysFont('Comic Sans MS', 30)
    # maak een leeg canvas (wit scherm)
    canvas = pg.display.set_mode((canvasWidth, canvasHeight))
    slider = Slider(canvas, 520, 200-5, 160, 10, min=5, max=160, step=1)
    slider_back = pg.Rect(520, 200-1, 160, 2)
    output = TextBox(canvas, 475, 200-12, 36, 24, fontSize=15)
    slider.setValue(maxAfstand)
    # maak een klok om de tijd bij te houden (nodig om scherm te verversen)
    clock = pg.time.Clock()
    while True:
        x = ser.readline().decode('ascii')  # Haalt /b,r,n weg en geeft stringwaarde terug

        if "A" in x:
            a = int(x[1:])
            print(a)
        elif "T" in x:
            t1 = x[1:]
            t = int(t1)
            print(t)
        elif "L" in x:
            intensity = int(x[1:])
            print(intensity)
        array_temp1.append(t)
        array_light1.append(intensity)
        if a in range(40, maxAfstand):
            isUitgerold = True
        elif a in range(10, 39):
            print("UITROLLEN OF FOUT")
        elif a in range(0, 9):
            isUitgerold= False
        # zorgt ervoor dat de array nooit langer dan 10 is
        if len(array_temp1) > 10:
            del array_temp1[0]
        if len(array_light1) > 10:
            del array_light1[0]
        # als temperatuur of licht de gegeven waardes overschrijden en het scherm op auto staat doe het scherm dan naar beneden
        # kijkt naar de waarde van het licht en bepaalt of het scherm in of uit moet rollen
        if intensity in range(1, 599) and t in range(-50, 0):
            if auto1 == True:
                if isUitgerold:

                    ser2.write(b'f')  # f is het flikkeren van het gele licht
                    ser2.write(b'y')  # y is de kleur groen LED

                    isUitgerold = False
                    intensity = 0
                    t = 0
                    a = 0
                    print("A")
                else:
                    pass
        elif intensity in range(1, 599) and t in range(25, 100):
            if auto1 == True:
                if isUitgerold:
                    pass
                else:

                    ser2.write(b'f')  # f is het flikkeren van het gele licht
                    ser2.write(b'r')  # r is de kleur rood LED

                    isUitgerold = True
                    intensity = 0
                    a = 0
                    t = 0
                    print("B")
        elif intensity in range(1, 599) and t in range(1, 25):
            if auto1 == True:
                if isUitgerold:

                    ser2.write(b'f')  # f is het flikkeren van het gele licht
                    ser2.write(b'y')  # y is de kleur groen LED

                    isUitgerold = False
                    intensity = 0
                    a = 0
                    t = 0
                    print("C")
                else:
                    pass
        elif intensity in range(600, 1000) and t in range(25, 100):
            if auto1 == True:
                if isUitgerold:
                    pass
                else:

                    ser2.write(b'f')  # f is het flikkeren van het gele licht
                    ser2.write(b'r')  # r is de kleur rood LED

                    isUitgerold = True
                    intensity = 0
                    a = 0
                    t = 0
                    print("D")
        elif intensity in range(600, 1000) and t in range(-50, 0):
            if auto1 == True:
                if isUitgerold:

                    ser2.write(b'f')  # f is het flikkeren van het gele licht
                    ser2.write(b'y')  # y is de kleur groen LED

                    isUitgerold = False
                    intensity = 0
                    a = 0
                    t = 0
                    print("E")
                else:
                    pass
        elif intensity in range(600, 1000) and t in range(1, 25):
            if auto1 == True:
                if isUitgerold:
                    pass
                else:

                    ser2.write(b'f')  # f is het flikkeren van het gele licht
                    ser2.write(b'r')  # r is de kleur rood LED

                    isUitgerold = True
                    intensity = 0
                    a = 0
                    t = 0
                    print("F")
        else:
            print("WAARDES DOORVOEREN, ERROR")
        #time.sleep(5)
        # geeft de achtrergrond een grijze kleur
        canvas.fill((200,200,200))
        if sunscreen1 == True:
            color_up_1 = color_green
            color_down_1 = color_red
        else:
            color_up_1 = color_red
            color_down_1 = color_green
        # haalt de (x,y) coordianten van de muis op
        mouse = pg.mouse.get_pos()
        # voor alle evenementen die plaatsvinden run deze code
        for ev in pg.event.get():
            # als er op het kruisje geklikt word sluit dan de pygame instance af
            if ev.type == pg.QUIT:
                pg.quit()
            # als er op de muis geklikt word loop dan de volgende code bij langs
            if ev.type == pg.MOUSEBUTTONDOWN:
                # als er op de auto cirkel geklikt word verander de variabele auto1 naar het tegenovergestelde van wat het op dat gegeven moment is
                if detectMouseInCircle(autoButton1[0], autoButton1[1], mouse):
                    print('circle1')
                    auto1 = not auto1
                # als er op de omlaag knop geklikt word verander de variabele auto1 naar False en de variabele sunscreen1 ook naar False
                if detectMouseInTriangle(info_knop1Triangle_omlaag, mouse) == True:
                    print('triangle2.1')
                    auto1 = False
                    sunscreen1 = False

                    ser2.write(b'f')  # f is het flikkeren van het gele licht
                    ser2.write(b'y')  # y is de kleur groen LED

                # als er op de omlaag knop geklikt word verander de variabele auto1 naar False en de variabele sunscreen1 naar True
                if detectMouseInTriangle(info_knop1Triangle_omhoog, mouse) == True:
                    print('triangle1.1')
                    auto1 = False
                    sunscreen1 = True

                    ser2.write(b'f')  # f is het flikkeren van het gele licht
                    ser2.write(b'r')  # r is de kleur rood LED

                # als er op de grafiek knop geklikt word maak dan een grafiek in een apart grafiek window
                if graph_temp1.collidepoint(mouse) == True:
                    print('graph')
                    # data voor de x as
                    x = [1,2,3,4,5,6,7,8,9,10]
                    # data voor de y as
                    y = array_temp1
                    # plot grafiek (splice de data voor de x as op basis van hoeveel data er in de data van de y as staat)
                    mpl.plot(x[0:len(y)], y)
                    # naam van de x as
                    mpl.xlabel('x')
                    # naam van de y as
                    mpl.ylabel('temperatuur (Celcius)')
                    # de naam van de grafiek
                    mpl.title('temperatuur grafiek')
                    # grafiek limits
                    mpl.xlim(0,10)
                    # laat de grafiek zien
                    mpl.show()

                if graph_light1.collidepoint(mouse) == True:
                    print('graph')
                    # data voor de x as
                    x = [1,2,3,4,5,6,7,8,9,10]
                    # data voor de y as
                    y = array_light1
                    # plot grafiek (splice de data voor de x as op basis van hoeveel data er in de data van de y as staat)
                    mpl.plot(x[0:len(y)], y)
                    # naam van de x as
                    mpl.xlabel('x')
                    # naam van de y as
                    mpl.ylabel('lichtintensiteit (klux)')
                    # de naam van de grafiek
                    mpl.title('lichtintensiteit')
                    # grafiek limits
                    mpl.xlim(0,10)
                    # laat de grafiek zien
                    mpl.show()
                slider.listen(ev)
                slider.draw()
                output.setText(slider.getValue())
                output.draw()
        slider.listen(ev)
        slider.draw()
        output.setText(slider.getValue())
        maxAfstand = slider.getValue()
        output.draw()
        #pg.draw.rect(canvas,color_dark,[info_graph_temp[0],info_graph_temp[2],info_graph_temp[4],info_graph_temp[5]])
        #pg.draw.rect(canvas,color_dark,[info_graph_light[0],info_graph_light[2],info_graph_light[4],info_graph_light[5]])
        # teken de omhoog en omlaag knoppen op het scherm
        pg.draw.polygon(canvas, color_down_1, info_knop1Triangle_omlaag)
        pg.draw.polygon(canvas, color_up_1, info_knop1Triangle_omhoog)
        # teken de knoppen voor de grafieken op het scherm
        pg.draw.rect(canvas, color_dark, graph_temp1)
        pg.draw.rect(canvas, color_dark, graph_light1)
        pg.draw.rect(canvas, (0,0,0), slider_back)
        #textSurf = font.render(str(a), False, (0, 0, 0))
        #canvas.blit(textSurf,(0,0))
        # als er over de auto cirkel gehovered word met de muis teken dan de cirkel afhankelijk van of auto aanstaat of niet
        if detectMouseInCircle(autoButton1[0], autoButton1[1], mouse):
            # als auto aan staat teken de cirkel dan met de color_greenDark kleur
            if auto1 == True:
                pg.draw.circle(canvas, color_greenDark, autoButton1[0], autoButton1[1])
            # als auto niet aan staat teken de cirkel dan met de color_redDark kleur
            else:
                pg.draw.circle(canvas, color_redDark, autoButton1[0], autoButton1[1])
        # als er niet over de auto cirkel gehovered word met de muis teken dan de cirkel afhankelijk van of auto aanstaat of niet
        else:
            # als auto aan staat teken de cirkel dan met de color_green kleur
            if auto1 == True:
                pg.draw.circle(canvas, color_green, autoButton1[0], autoButton1[1])
            # als auto niet aan staat teken de cirkel dan met de color_red kleur
            else:
                pg.draw.circle(canvas, color_red, autoButton1[0], autoButton1[1])
        # update het scherm
        pg.display.flip()
        # herhaal code elke 1/60 second
        clock.tick(1)
    pg.quit()
# start code
main()
