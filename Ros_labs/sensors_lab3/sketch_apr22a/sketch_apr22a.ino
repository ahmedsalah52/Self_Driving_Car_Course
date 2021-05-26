#include <TimerOne.h>

const byte interruptPinA_R = 2;
const byte interruptPinB_R = 3;

const byte interruptPinA_L = 2;
const byte interruptPinB_L = 3;

float velocity;
long count_R;
bool Dir_R;
void setup() {


  int freq = 30;
  pinMode(interruptPinA_R, INPUT_PULLUP);
  pinMode(interruptPinB_R, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPinA_R), catch_A, CHANGE );
  attachInterrupt(digitalPinToInterrupt(interruptPinB_R), catch_B, CHANGE );
  
  Timer1.initialize(1000000/freq);
  Timer1.attachInterrupt(send_msg); // blinkLED to run every 0.15 seconds

  Serial.begin(9600);
  
}

void loop() {

  

}


void send_msg()
{
  //Serial.println(Dir_R);
  //Serial.println(count_R);
  velocity = ((count_R * freq )/(1640.0))*(2.0*3.14*0.15);
  Serial.print(velocity);
  Serial.print(" , ");
  Serial.println(velocity);


  count_R = 0;

}


void catch_A(void) {
 if(((!digitalRead(interruptPinB_R)) && digitalRead(interruptPinA_R)) || ((!digitalRead(interruptPinA_R)) && digitalRead(interruptPinB_R)))
 {
    Dir_R = 1;
    count_R++;

  }
  else
  {

    Dir_R = 0;
    count_R--;

  }
  
}


void catch_B(void) {
 if(((!digitalRead(interruptPinA_R)) && digitalRead(interruptPinB_R)) || ((!digitalRead(interruptPinB_R)) && digitalRead(interruptPinA_R)))
 {
    Dir_R = 0;
    count_R--;

  }
  else
  {
    Dir_R = 1;
    count_R++;

  }
  
}
