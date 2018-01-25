#ifndef MONSTER_H
#define MONSTER_H

#include <Arduino.h>

#define A_PIN_1 7
#define A_PIN_2 4
#define B_PIN_1 8
#define B_PIN_2 9
#define PWM_PIN_1 5
#define PWM_PIN_2 6
#define CS_PIN_1 2
#define CS_PIN_2 3
#define EN_PIN_1 0
#define EN_PIN_2 1
#define STAT_PIN 13


class Monster {
private:
  const int _inApin[2] = { A_PIN_1, A_PIN_2 };
  const int _inBpin[2] = { B_PIN_1, B_PIN_2 };
  const int _pwmpin[2] = { PWM_PIN_1, PWM_PIN_2 };
  const int _cspin[2] = { CS_PIN_1, CS_PIN_2 };
  const int _enpin[2] = { EN_PIN_1, EN_PIN_2 };

public:
  Monster();
  void stopA();
  void stopB();
  void stop();
  void startA();
  void startB();
  void setSpeedA(uint8_t speed);
  void setSpeedB(uint8_t speed);

};


#endif
