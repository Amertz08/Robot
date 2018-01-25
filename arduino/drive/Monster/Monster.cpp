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

void Monster::stopA()
{
  digitalWrite(this->_inApin[0], LOW);
  digitalWrite(this->_inApin[1], LOW);
}

void Monster::stopB()
{
  digitalWrite(this->_inBpin[0], LOW);
  digitalWrite(this->_inBpin[1], LOW);
}

void Monster::stop()
{
  this->stopA();
  this->stopB();
}

void Monster::startA()
{
  digitalWrite(this->_inApin[0], HIGH);
  digitalWrite(this->_inApin[1], HIGH);
}

void Monster::startB()
{
  digitalWrite(this->_inBpin[0], HIGH);
  digitalWrite(this->_inBpin[1], HIGH);
}

void Monster::setSpeedA(uint8_t speed)
{
  this->startA();
  analogWrite(this->_pwmpin[0], speed);
}

void Monster::setSpeedB(uint8_t speed)
{
  this->startB();
  analogWrite(this->_pwmpin[1], speed);
}
