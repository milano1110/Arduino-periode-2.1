// Bibliotheek voor het werken met een analoge thermometer (Troyka-module)
#include <TroykaThermometer.h>
#define ldrPin A1

// Een object maken om met een analoge thermometer te werken
// En geef het de pincode van het uitgangssignaal door
TroykaThermometer thermometer(A0);
// Variabele voor het aantal seconden om gemiddelde te berekenen.
int aantalSecG = 40;
float aantal = 0.0; 

// Pin nummers definieëren
const int trigPin = 9;
const int echoPin = 10;
// Variabelen definieëren
long duration;
int distance;

void setup()
{
  // Open de seriële poort
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(ldrPin, INPUT);
  Serial.begin(9600);
  
}

void loop()
{
  Temp();
  Afst();
  Licht();
  delay(60000);
   
}

void Temp() {
  // Temperatuur
  thermometer.read();
  float total = 0.0;
  for(int i = 0;i < 40;i++){ // accumulate 16 readings in total
    total += thermometer.getTemperatureC();
  }
  Serial.print("T");  
  Serial.println(total / 40); // divide by 16 and print
}

void Afst() {
  // Afstand
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034/2;
  Serial.print("A");
  Serial.println(distance);
}

void Licht() {
  //Lichtintensiteit
  int total2 = 0;
  int ldrIntensity = analogRead(ldrPin);
  for(int i = 0;i < 30;i++) {
    total2 += ldrIntensity;
  }
  Serial.print("L");
  Serial.println(total2 / 30);
}
