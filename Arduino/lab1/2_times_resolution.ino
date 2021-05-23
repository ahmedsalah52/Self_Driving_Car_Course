#encoder_counter, it counts the rising edges of the two channels 



const byte interruptPinA = 2;
const byte interruptPinB = 3;

long count;
bool Dir;
void setup() {
  
  pinMode(interruptPinA, INPUT_PULLUP);
  pinMode(interruptPinB, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPinA), catch_A, RISING );
  attachInterrupt(digitalPinToInterrupt(interruptPinB), catch_B, RISING );
  Serial.begin(9600);
  
}

void loop() {
  
  Serial.println(Dir);
  Serial.println(count);

}

void catch_A(void) {
  if(digitalRead(interruptPinB))
  {
    count++;
    Dir = 1;
  }
  else
  {
    Dir = 0;
    count--;
  }
  
}


void catch_B(void) {
  if(!digitalRead(interruptPinA))
  {
    count++;
    Dir = 1;
  }
  else
  {
    Dir = 0;
    count--;
  }
  
}
