#include "Monster.h"

Monster::Monster()
{
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

void Monster::stopMotor(uint8_t motor)
{
  this->driveMotor(motor, BRAKE, 0);
}

void Monster::stop()
{
  this->stopMotor(0);
  this->stopMotor(1);
}

bool Monster::_validateSpeed(uint8_t speed)
{
  return (MIN_SPEED <= speed && speed <= MAX_SPEED);
}

void Monster::setSpeed(uint8_t motor, uint8_t speed)
{
  if (!this->_validateSpeed(speed)) {
    throw Exception("Invalid speed");
  }
  analogWrite(this->_pwmpin[motor], speed);
}

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
