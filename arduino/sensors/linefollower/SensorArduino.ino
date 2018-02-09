#include <Wire.h>
#include "sensorbar.h"
#include "smoothing.h" //not sure how we're including with the make file

#define motor_arduino_address 8

#define IDLE_STATE 0
#define READ_LINE 1
#define GO_FORWARD 2
#define GO_LEFT 3
#define GO_RIGHT 4

//Pins
const unit8_t TRIG_PIN = 12;
const unit8_t ECHO_PIN = 13;

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
const uint8_t MAX_OBSTACLE_DISTANCE = 8;

SensorBar mySensorBar(SX1509_ADDRESS);
SMOOTHING ultraSmooth = SMOOTHING(5);

void setup() {
  Serial.begin(9600);
  Serial.println("Program started.");
  Serial.println();

  pinMode(TRIG_PIN, OUTPUT);
  digitalWrite(TRIG_PIN, LOW);

  mySensorBar.setBarStrobe();
  mySensorBar.clearInvertBits();
  returnStatus = mySensorBar.begin();
  if(returnStatus) {
    Serial.println("sx1509 IC communication OK");
  }
  else {
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
    if(ultraSonic() > MAX_OBSTACLE_DISTANCE) {
      if(mySensorBar.getDensity() < 8 && mySensorBar.getDensity() > 0) {
        nextState = GO_FORWARD;
        if(mySensorBar.getPosition() < -50) {
          nextState = GO_LEFT;
        }
        if(mySensorBar.getPosition() > 50) {
          nextState = GO_RIGHT;
        }
      }
      else if(mySensorBar.getDensity() == 0) {
        nextState = findLine();
      }
      else {
        nextState = IDLE_STATE;
      }
    }
    else {
      stopMotors();
      nextState = READ_LINE;
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
void writeSpeed(int writeAddress, uint8_t leftDirection, uint8_t leftSpeed, uint8_t rightDirection, uint8_t rightSpeed) {
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
void driveBot(int16_t driveInput) {
  uint8_t leftVar;
  uint8_t rightVar;
  uint8_t directionVar = 0;
  if(driveInput < 0) {
    directionVar = 1;
    driveInput = driveInput * -1;
  }
  leftVar = (uint8_t)driveInput;
  rightVar = (uint8_t)driveInput;
}

void leftTurn() {
  writeSpeed(motor_arduino_address, FWD, 0, FWD, MAX_SPEED);
}

void rightTurn() {
  writeSpeed(motor_arduino_address, FWD, MAX_SPEED, FWD, 0);
}

uint8_t findLine() {
  while(mySensorBar.getDensity() == 0) {
    writeSpeed(motor_arduino_address, BKWD, MAX_SPEED * 0.5, BKWD, MAX_SPEED * 0.5);
  }
  stopMotors();
  if(mySensorBar.getPosition() < -50) {
        return GO_LEFT;
  }
  if(mySensorBar.getPosition() > 50) {
        return GO_RIGHT;
  }
}

uint16_t ultraSonic() {
  unsigned long t1;
  unsigned long t2;
  unsigned long pulse_width;
  uint16_t cm;
  uint16_t average;

  /* Hold the trigger pin high for at least 10 us */
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  /* Wait for pulse on echo pin */
  while ( digitalRead(ECHO_PIN) == 0 );

  /*
  * Measure how long the echo pin was held high (pulse width)
  * Note: the micros() counter will overflow after ~70 min
  */
  t1 = micros();
  while ( digitalRead(ECHO_PIN) == 1);
  t2 = micros();
  pulse_width = t2 - t1;
  cm = pulse_width / 58;
  average = ultraSmooth.smooth(cm);
  return average;
}
