#include "Monster.h"

Monster::Monster(uint8_t mode)
{
  this->_mode = mode;
  pinMode(STAT_PIN, OUTPUT);

  for (int i = 0; i < 2; i++) {
    // Set as output
    pinMode(this->_Apins[i], OUTPUT);
    pinMode(this->_Bpins[i], OUTPUT);
    pinMode(this->_pwmin[i], OUTPUT);
    pinMode(this->_cspin[i], OUTPUT);
    pinMode(this->_enpin[i], OUTPUT);

    // Initialized braked
    digitalWrite(this->_Apins[i], LOW);
    digitalWrite(this->_Apins[i], LOW);

    // Enable
    digitalWrite(this->_enpin[i], HIGH);
  }

}

Monster::~Monster() {
  this->stop();
}

/**
  Stops the given motor
  @param motor - motor 0 or 1
*/
void Monster::stopMotor(uint8_t motor)
{
  this->driveMotor(motor, BRAKE, 0);
}

/**
  Stops all motors
*/
void Monster::stop()
{
  this->stopMotor(0);
  this->stopMotor(1);
}

/**
  Checks if given speed is valid
*/
bool Monster::_validateSpeed(uint8_t speed)
{
  return (MIN_SPEED <= speed && speed <= MAX_SPEED);
}

/**
  Set speed for the given motor
  @param motor - motor 0 or 1
  @param speed - speed to move at 0 to 255
*/
void Monster::setSpeed(uint8_t motor, uint8_t speed)
{
  if (!this->_validateSpeed(speed)) {
    throw Exception("Invalid speed");
  }
  analogWrite(this->_pwmpin[motor], speed);
}

/**
  Drives vehicle forward at given speed
  @param speed - speed to move at 0 to 255
*/
void Monster::forward(uint8_t speed)
{
  switch (this->_mode) {
    case MIXED:
      this->driveMotor(0, CW, speed);
      this->driveMotor(1, CCW, speed);
      break
    case LEFT:
      this->driveMotor(0, CW, speed);
      this->driveMotor(1, CW, speed);
      break;
    case RIGHT:
      this->driveMotor(0, CCW, speed);
      this->driveMotor(1, CCW, speed);
      break;
    default:
      throw Exception("Invalid Mode");
  }
}

/**
  Drives vehicle backward at given speed
  @param speed - speed to move at 0 to 255
*/
void Monster::backward(uint8_t speed)
{
  switch (this->_mode) {
    case MIXED:
      this->driveMotor(0, CCW, speed);
      this->driveMotor(1, CW, speed);
      break
    case LEFT:
      this->driveMotor(0, CCW, speed);
      this->driveMotor(1, CCW, speed);
      break;
    case RIGHT:
      this->driveMotor(0, CW, speed);
      this->driveMotor(1, CW, speed);
      break;
    default:
      throw Exception("Invalid Mode");
  }
}

/*
  Drive given motor in the given direction for given speed
  @param motor - 0 or 1
  @param direction - CW, CCW, BRAKE
  @param speed - speed to move at 0 to 255
*/
void Monster::driveMotor(uint8_t motor, uint8_t direction, uint8_t speed)
{
  switch (direction) {
    case CW:
      digitalWrite(this->_Apins[motor], LOW);
      digitalWrite(this->_Bins[motor], HIGH);
      break;
    case CCW:
      digitalWrite(this->_Apins[motor], HIGH);
      digitalWrite(this->_Bpins[motor], LOW);
      break;
    case BRAKE:
      digitalWrite(this->_Apins[motor], LOW);
      digitalWrite(this->_Bpins[motor], LOW);
      break;
    default:
      throw Exception("Invalid direction");
  }
  this->setSpeed(motor, speed);
}
