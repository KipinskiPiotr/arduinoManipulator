#include <Servo.h>

Servo servos[4];
String data = "nothing";

void moveServo(int num, int angle){
  Serial.print("Moving servo " + String(num) + " to " + String(angle) + " angle.");
  servos[num+1].write(angle);
}

int handleCommand(String com){
  //Serial.println("Handling command: " + com);
  int num = com.substring(0,1).toInt(); // Assuming 1 digit servo numbers
  int angle = com.substring(2).toInt();
  moveServo(num, angle);
}

void setup() {
  servos[0].attach(3);
  servos[1].attach(5);
  servos[2].attach(6);
  servos[3].attach(9);
  Serial.begin(115200);
}

void loop() {
  if(Serial.available() > 0){
    data = Serial.readStringUntil('|');
    handleCommand(data);
  }
  delay(30);
}