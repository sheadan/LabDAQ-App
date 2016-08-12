//// ArduinoDAQ
// Kevin Hughes 2012

//// Constants
int BAUDRATE = 115200;
int DELAY_BETWEEN_ANALOG_READ=1

//// Alarm functionality
void soundTheAlarm() {
  //add in here what you want to happen when the alarm sounds
}

void setup() {

  // All pins to input
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);

  // Init Serial
  Serial.begin(BAUDRATE);

}// end setup

void loop() {

  if(Serial.available()) {

    int signal = Serial.read();

    if(signal == 119) {

      Serial.println( analogRead(A0) );    delayMicroseconds(DELAY_BETWEEN_ANALOG_READ);
      Serial.println( analogRead(A1) );    delayMicroseconds(DELAY_BETWEEN_ANALOG_READ);
      Serial.println( analogRead(A2) );    delayMicroseconds(DELAY_BETWEEN_ANALOG_READ);
      Serial.println( analogRead(A3) );    delayMicroseconds(DELAY_BETWEEN_ANALOG_READ);
      Serial.println( analogRead(A4) );    delayMicroseconds(DELAY_BETWEEN_ANALOG_READ);
      Serial.println( analogRead(A5) );    delayMicroseconds(DELAY_BETWEEN_ANALOG_READ);
      Serial.println( millis() );   delayMicroseconds(DELAY_BETWEEN_ANALOG_READ);

    }

    if(signal == 97) {
      soundTheAlarm()
    }



    }//end if
  }// end if
}// end loop
