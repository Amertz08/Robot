#include <Monster.h>
#include <Wire.h>

#define LEFT_MOTOR 1
#define RIGHT_MOTOR 0

Monster shield = Monster(MIXED);

uint8_t m_leftDirection;
uint8_t m_leftSpeed;
uint8_t m_rightDirection;
uint8_t m_rightSpeed;

void setup() {
  Wire.begin(8);
  Wire.onReceive(receiveEvent);
  Serial.begin(9600);
  m_leftDirection = 0;
  m_leftSpeed = 0;
  m_rightDirection = 0;
  m_rightSpeed = 0;
  shield.stop();
}

void loop() {
  Serial.print(m_leftDirection);
  Serial.print(" ");
  Serial.print(m_leftSpeed);
  Serial.print(" ");
  Serial.print(m_rightDirection);
  Serial.print(" ");
  Serial.print(m_rightSpeed);
  Serial.println();
}

void receiveEvent(int bytesToRead) {
  m_leftDirection = Wire.read();
  m_leftSpeed = Wire.read();
  m_rightDirection = Wire.read();
  m_rightSpeed = Wire.read();

  shield.driveMotor(LEFT_MOTOR, m_leftDirection, m_leftSpeed);
  shield.driveMotor(RIGHT_MOTOR, m_rightDirection, m_rightSpeed);
}
