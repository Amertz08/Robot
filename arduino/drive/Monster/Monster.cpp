#include "Monster.h"

Monster::Monster(uint8_t mode)
{
  this->_validateMode(mode);
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

void Monster::_validateMode(uint8_t mode)
{
  switch (mode) {
    case MIXED:
      break;
    case LEFT:
      break;
    case RIGHT:
      break;
    default:
      throw Exception("Invalid mode");
  }
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
  if (this->_mode == MIXED) {
    this->driveRight(speed);
    this->driveLeft(speed * -1);
  } else {
    this->driveRight(speed);
    this->driveLeft(speed);
  }
}

/**
  Drives vehicle backward at given speed
  @param speed : speed to move at 0 to 255
*/
void Monster::backward(uint8_t speed)
{
  if (this->_mode == MIXED) {
    this->driveRight(speed * -1);
    this->driveLeft(speed);
  } else {
    this->driveRight(speed * -1);
    this->driveLeft(speed * - 1);
  }
}

/*
  Drives motor(s) on right side
  @param speed : -255 to 255
*/
void Monster::driveRight(uint8_t speed)
{
  uint8_t direction;

  if (speed < 0) {
    direction = CW;
  } else if (speed > 0) {
    direction = CCW;
  } else {
    direction = BRAKE;
  }
  this->driveMotor(1, direction, abs(speed));
  if (this->_mode != MIXED) {
    // If not in mixed you need to set both motors
    this->driveMotor(0, direction, abs(speed));
  }
}

/*
  Drives motor(s) on left side
  @param speed : -255 to 255
*/
void Monster::driveLeft(uint8_t speed)
{
  uint8_t direction;

  if (speed < 0) {
    direction = CCW;
  } else if (speed > 0) {
    direction = CW;
  } else {
    direction = BRAKE;
  }
  this->driveMotor(0, direction, abs(speed));
  if (this->_mode != MIXED) {
    // If not in mixed you need to set both motors
    this->driveMotor(1, direction, abs(speed));
  }
}

/*
  Turn vehicle left at given speed
  @param speed : speed to drive motors 0 to 255
*/
void Monster::turnLeft(uint8_t speed)
{
  this->driveLeft(speed * -1);
  this->driveRight(speed);
}

/*
  Turn vehicle right at given speed
  @param speed - speed to drive motors 0 to 255
*/
void Monster::turnRight(uint8_t speed)
{
  this->driveLeft(speed);
  this->driveRight(speed * -1);
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
