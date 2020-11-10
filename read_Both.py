import serial  # Importeerd module serial
import time  # Importeerd module time


w = None
ser = serial.Serial('COM4', 9600)  # Opent poort 9600 op COM4
ser2 = serial.Serial('COM3', 9600)  # Opent poort 9600 op COM3
a = 0
t = 0
t1 = 0
intensity = 0
uitgerold = False
while 1:  # Altijd doorgaan
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

    if a in range(40, 10000):
        uitgerold = True
    elif a in range(10, 39):
        print("UITROLLEN OF FOUT")
    elif a in range(1, 9):
        uitgerold = False

    # kijkt naar de waarde van het licht en bepaalt of het scherm in of uit moet rollen
    if intensity in range(1, 599) and t in range(-50, 0):
        if uitgerold:
            ser2.write(b'f')  # f is het flikkeren van het gele licht
            ser2.write(b'y')  # y is de kleur groen LED
            uitgerold = False
            intensity = 0
            t = 0
            a = 0
            print("A")
        else:
            pass
    elif intensity in range(1, 599) and t in range(25, 100):
        if uitgerold:
            pass
        else:
            ser2.write(b'f')  # f is het flikkeren van het gele licht
            ser2.write(b'r')  # r is de kleur rood LED
            uitgerold = True
            intensity = 0
            a = 0
            t = 0
            print("B")
    elif intensity in range(1, 599) and t in range(1, 25):
        if uitgerold:
            ser2.write(b'f')  # f is het flikkeren van het gele licht
            ser2.write(b'y')  # y is de kleur groen LED
            uitgerold = False
            intensity = 0
            a = 0
            t = 0
            print("C")
        else:
            pass
    elif intensity in range(600, 1000) and t in range(25, 100):
        if uitgerold:
            pass
        else:
            ser2.write(b'f')  # f is het flikkeren van het gele licht
            ser2.write(b'r')  # r is de kleur rood LED
            uitgerold = True
            intensity = 0
            a = 0
            t = 0
            print("D")
    elif intensity in range(600, 1000) and t in range(-50, 0):
        if uitgerold:
            ser2.write(b'f')  # f is het flikkeren van het gele licht
            ser2.write(b'y')  # y is de kleur groen LED
            uitgerold = False
            intensity = 0
            a = 0
            t = 0
            print("E")
        else:
            pass
    elif intensity in range(600, 1000) and t in range(1, 25):
        if uitgerold:
            pass
        else:
            ser2.write(b'f')  # f is het flikkeren van het gele licht
            ser2.write(b'r')  # r is de kleur rood LED
            uitgerold = True
            intensity = 0
            a = 0
            t = 0
            print("F")
    else:
        print("WAARDES DOORVOEREN, ERROR")
