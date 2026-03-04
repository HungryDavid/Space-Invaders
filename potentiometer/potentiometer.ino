#include <ResponsiveAnalogRead.h>

const int potPin = A0;
const int btnPin = 7;

int prevVal = 0;
int currVal = 0;

int btn = 0;

ResponsiveAnalogRead pot = ResponsiveAnalogRead(potPin, true);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
      Serial.setTimeout(1);
  pinMode(potPin, INPUT);
  pinMode(btnPin, INPUT_PULLUP); 

}

void loop() {
  // put your main code here, to run repeatedly:
    pot.update();
  currVal = pot.getValue();
  btn = digitalRead(btnPin);

  if (currVal != prevVal){
    prevVal = currVal;
    delay(3);
  }

  Serial.print(currVal); Serial.print(","); Serial.println(btn);

}
