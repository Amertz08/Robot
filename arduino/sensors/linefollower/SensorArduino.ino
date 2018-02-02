#include <Wire.h>
#include "sensorbar.h"

#define motor_arduino_address 8

#define IDLE_STATE 0
#define READ_LINE 1
#define GO_FORWARD 2
#define GO_LEFT 3
#define GO_RIGHT 4

const uint8_t SX1509_ADDRESS = 0x3E;

uint8_t state;
uint8_t returnStatus;

/*unnecessary at the moment*/
uint8_t m_leftDirection;
uint8_t m_leftSpeed;
uint8_t m_rightDirection;
uint8_t m_rightSpeed;

const uint8_t FWD = 0;
const uint8_t BKWD = 1;
const uint8_t MAX_SPEED = 150;

SensorBar mySensorBar(SX1509_ADDRESS);
  
void setup() {
  Serial.begin(9600);
  Serial.println("Program started.");
  Serial.println();
  mySensorBar.setBarStrobe();
  mySensorBar.clearInvertBits();
  returnStatus = mySensorBar.begin();
  if(returnStatus)
  {
    Serial.println("sx1509 IC communication OK");
  }
  else
  {
    Serial.println("sx1509 IC communication FAILED!");
  }
  Serial.println();
  Wire.begin(10);
  m_leftDirection = FWD;
  m_leftSpeed = 0;
  m_rightDirection = FWD;
  m_rightSpeed = 0;
  state = 0;
  
}

void loop() {
  //writeSpeed(motor_arduino_address, m_leftDirection, m_leftSpeed, m_rightDirection, m_rightSpeed);
  uint8_t nextState = state;
  uint8_t prevState = state;
    switch (state) {
  case IDLE_STATE:
    stopMotors();       // Stops both motors
    nextState = READ_LINE;
    prevState = IDLE_STATE;
    break;
  case READ_LINE:
    if( mySensorBar.getDensity() < 8 && mySensorBar.getDensity() > 0)
    {
      nextState = GO_FORWARD;
      if( mySensorBar.getPosition() < -50 )
      {
        nextState = GO_LEFT;
      }
      if( mySensorBar.getPosition() > 50 )
      {
        nextState = GO_RIGHT;
      }
    }
    else if(mySensorBar.getDensity() == 0)
    {
      nextState = findLine();
    }
    else
    {
      nextState = IDLE_STATE;
    }
    prevState = READ_LINE;
    break;
  case GO_FORWARD:
    driveBot(MAX_SPEED);
    nextState = READ_LINE;
    break;
  case GO_LEFT:
    leftTurn();
    nextState = READ_LINE;
    prevState = GO_LEFT;
    break;
  case GO_RIGHT:
    rightTurn();
    nextState = READ_LINE;
    prevState = GO_RIGHT;
    break;
  default:
    stopMotors();       // Stops both motors
    break;
  }
  state = nextState;
  delay(100);
}

/*Send speed and direction instructions to motor arduino*/
void writeSpeed(int writeAddress, uint8_t leftDirection, uint8_t leftSpeed, uint8_t rightDirection, uint8_t rightSpeed){
  Wire.beginTransmission(writeAddress);
  Wire.write(leftDirection);
  Wire.write(leftSpeed);
  Wire.write(rightDirection);
  Wire.write(rightSpeed);
  Wire.endTransmission();
}

void stopMotors() {
  writeSpeed(motor_arduino_address, FWD, 0, FWD, 0);
}

/*drive bot in a straight line*/
void driveBot(int16_t driveInput){
  uint8_t leftVar;
  uint8_t rightVar;
  uint8_t directionVar = 0;
  if(driveInput < 0){
    directionVar = 1;
    driveInput = driveInput * -1;
  }
  leftVar = (uint8_t)driveInput;
  rightVar = (uint8_t)driveInput;
}

void leftTurn(){
  writeSpeed(motor_arduino_address, FWD, 0, FWD, MAX_SPEED);
}

void rightTurn(){
  writeSpeed(motor_arduino_address, FWD, MAX_SPEED, FWD, 0);
}

uint8_t findLine(){
  while(mySensorBar.getDensity() == 0){
    writeSpeed(motor_arduino_address, BKWD, MAX_SPEED * 0.5, BKWD, MAX_SPEED * 0.5);
  }
  stopMotors();
  if( mySensorBar.getPosition() < -50 )
      {
        return GO_LEFT;
      }
  if( mySensorBar.getPosition() > 50 )
      {
        return GO_RIGHT;
      }
}
