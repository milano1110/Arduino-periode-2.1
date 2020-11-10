#define ledGroen 13
#define ledRood 12
#define ledGeel 10

void setup() {
  Serial.begin(9600);
  pinMode(ledGeel, OUTPUT);
  pinMode(ledGroen, OUTPUT);
  pinMode(ledRood, OUTPUT);
}

void loop() {
  char incomingByte;
    if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    if (incomingByte == 'r') {
      digitalWrite(ledRood, HIGH);
      digitalWrite(ledGroen, LOW);
      digitalWrite(ledGeel, LOW);  

    }
    else if (incomingByte == 'y') {
      digitalWrite(ledRood, LOW);
      digitalWrite(ledGroen, HIGH);
      digitalWrite(ledGeel, LOW);
    }
    else if(incomingByte== 'g') {
      digitalWrite(ledRood, LOW);
      digitalWrite(ledGroen, LOW);
      digitalWrite(ledGeel, HIGH);  
    }
    else if(incomingByte == 'f') {
      digitalWrite(ledRood, LOW);
      digitalWrite(ledGroen, LOW);
      for(int i=0; i <= 5; i++) {
      digitalWrite(ledGeel, HIGH);  
      delay(250);                     
      digitalWrite(ledGeel, LOW);
      delay(250);
      }
    }
    else {
      digitalWrite(ledRood, LOW);
      digitalWrite(ledGroen, LOW);
      digitalWrite(ledGeel, LOW);
    }
   }
   delay(5000);
}
