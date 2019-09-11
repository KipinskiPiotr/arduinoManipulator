#include <Servo.h>

Servo servos[5];
String data = "nothing";

void moveServo(int num, int angle){
  //Serial.print("Moving servo " + String(num) + " to " + String(angle) + " angle.");
  servos[num-1].write(angle);
}

int handleCommand(String com){
  //Serial.println("Handling command: " + com);
  int num = com.substring(0,1).toInt(); // Assuming 1 digit servo numbers
  int angle = com.substring(2).toInt();
  moveServo(num, angle);
}

void setup() {
  servos[0].attach(3);
  servos[0].write(90);
  servos[1].attach(5);
  servos[1].write(90);
  servos[2].attach(6);
  servos[2].write(90);
  servos[3].attach(9);
  servos[3].write(90);
  servos[4].attach(10);
  servos[4].write(90);
  Serial.begin(115200);
}

void loop() {
  if(Serial.available() > 0){
    data = Serial.readStringUntil('|');
    handleCommand(data);
  }
  delay(10);
}
