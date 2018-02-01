#include "Monster.h"

#define SPEED 120

Monster shield = Monster(MIXED);

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char inChar = Serial.read();

    switch (inChar) {
      case 'W':
        shield.forward(SPEED);
        break;
      case 'S':
        shield.backward(SPEED);
        break;
      case 'D':
        shield.driveLeft(SPEED);
        break;
      case 'A':
        shield.driveRight(SPEED);
        break;
      default:
        shield.stop();
        break;
    }
  }

}
