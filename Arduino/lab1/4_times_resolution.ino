#encoder_counter , it counts the rising and falling edges of the two channels 

const byte interruptPinA = 2;
const byte interruptPinB = 3;

long count;
bool Dir;
void setup() {
  
  pinMode(interruptPinA, INPUT_PULLUP);
  pinMode(interruptPinB, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPinA), catch_A, CHANGE );
  attachInterrupt(digitalPinToInterrupt(interruptPinB), catch_B, CHANGE );
  Serial.begin(9600);
  
}

void loop() {
  
  Serial.println(Dir);
  Serial.println(count);

}

void catch_A(void) {
 if(((!digitalRead(interruptPinB)) && digitalRead(interruptPinA)) || ((!digitalRead(interruptPinA)) && digitalRead(interruptPinB)))
 {
    Dir = 1;
    count++;

  }
  else
  {

    Dir = 0;
    count--;

  }
  
}


void catch_B(void) {
 if(((!digitalRead(interruptPinA)) && digitalRead(interruptPinB)) || ((!digitalRead(interruptPinB)) && digitalRead(interruptPinA)))
 {
    Dir = 0;
    count--;

  }
  else
  {
Dir = 1;
    count++;

  }
  
}
