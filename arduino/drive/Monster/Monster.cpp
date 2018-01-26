#include "Monster.h"

Monster::Monster()
{
  pinMode(STAT_PIN, OUTPUT);

  for (int i = 0; i < 2; i++) {
    // Set as output
    pinMode(this->_inApin[i], OUTPUT);
    pinMode(this->_inBpin[i], OUTPUT);
    pinMode(this->_pwmin[i], OUTPUT);

    // Initialized braked
    digitalWrite(this->_inApin[i], LOW);
    digitalWrite(this->_inBpin[i], LOW);
  }
}

Monster::~Monster() {
  this->stop();
}

void Monster::stopOne()
{
  digitalWrite(this->_inApin[0], LOW);
  digitalWrite(this->_inBpin[0], LOW);
}

void Monster::stopTwo()
{
  digitalWrite(this->_inApin[1], LOW);
  digitalWrite(this->_inBpin[1], LOW);
}

void Monster::stop()
{
  this->stopA();
  this->stopB();
}

void Monster::startOne()
{
  digitalWrite(this->_inApin[0], HIGH);
  digitalWrite(this->_inBpin[0], HIGH);
}

void Monster::startTwo()
{
  digitalWrite(this->_inApin[1], HIGH);
  digitalWrite(this->_inBpin[1], HIGH);
}

bool Monster::_validateSpeed(uint8_t speed)
{
  return (MIN_SPEED <= speed && speed <= MAX_SPEED);
}

void Monster::setSpeedOne(uint8_t speed)
{
  if (!this->_validateSpeed(speed)) {
    throw Exception("Invalid speed");
  }
  this->startA();
  analogWrite(this->_pwmpin[0], speed);
}

void Monster::setSpeedTwo(uint8_t speed)
{
  if (!this->_validateSpeed(speed)) {
    throw Exception("Invalid speed");
  }
  this->startB();
  analogWrite(this->_pwmpin[1], speed);
}
