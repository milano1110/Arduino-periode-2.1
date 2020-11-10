import serial  # Importeerd module serial
import time  # Importeerd module time

uitgerold = False
w = None
a = 0
t = 0.0
intensity = 0
ser = serial.Serial('COM4', 9600)  # Opent poort 9600 op COM4
ser2 = serial.Serial('COM3', 9600)  # Opent poort 9600 op COM3
while 1:  # Altijd doorgaan
    x = ser.readline().decode('ascii')  # Haalt /b,r,n weg en geeft stringwaarde terug

    if "A" in x:
        a = int(x[1:])
        print(a)
    elif "T" in x:
        t1 = x[1:]
        t = float(t1)
        print(t)
    elif "L" in x:
        intensity = int(x[1:])
        print(intensity)

    # kijkt naar de waarde van het licht en bepaalt of het scherm in of uit moet rollen
    if -50.0 < t < 10.0:
        if uitgerold:
            ser2.write(b'f')  # f is het flikkeren van het gele licht
            ser2.write(b'y')  # y is de kleur groen LED
            uitgerold = False
        else:
            pass
    elif 10.0 < t < 14.99:
        if uitgerold:
            pass
        else:
            ser2.write(b'f')  # f is het flikkeren van het gele licht
            ser2.write(b'r')  # r is de kleur rood LED
            uitgerold = True
    elif 15.00 < t < 30.00:
        if uitgerold:
            pass
        else:
            ser2.write(b'f')  # f is het flikkeren van het gele licht
            ser2.write(b'r')  # r is de kleur rood LED
            uitgerold = True
    else:
        print("ERROR")
