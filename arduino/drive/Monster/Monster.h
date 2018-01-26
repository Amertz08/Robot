/**
* ASSUMPTIONS
* A pin for given motor is POSITIVE lead
* B pin for given motor is NEGATIVE lead
*
* MODES
*   LEFT - Two motors on left side of vehicle
*   RIGHT - Two motors on right side of vehicle
*   MIXED - Two motors on opposite sides - Motor 1 being left and Motor 2 being right
*/

#ifndef MONSTER_H
#define MONSTER_H

#include <Arduino.h>

// MOTOR 1
#define A_PIN_1 7
#define B_PIN_1 8
#define PWM_PIN_1 5
#define CS_PIN_1 2
#define EN_PIN_1 0
#define M1_ENC_A_PIN_1 0
#define M1_ENC_A_PIN_2 0
#define M1_ENC_B_PIN_1 0
#define M1_ENC_B_PIN_2 0
// MOTOR 2
#define A_PIN_2 4
#define B_PIN_2 9
#define PWM_PIN_2 6
#define CS_PIN_2 3
#define EN_PIN_2 1
#define M2_ENC_A_PIN_1 0
#define M2_ENC_A_PIN_2 0
#define M2_ENC_B_PIN_1 0
#define M2_ENC_B_PIN_2 0

#define STAT_PIN 13
#define MIN_SPEED 0
#define MAX_SPEED 255
// Direction
#define BRAKE 0
#define CW 1
#define CCW 2
// Modes
#define MIXED 0
#define LEFT 1
#define RIGHT 2


class Monster {
private:
  // Motor 1 = index 0; Motor 2 = index 1
  const uint8_t _Apins[2] = { A_PIN_1, A_PIN_2 };
  const uint8_t _Bpins[2] = { B_PIN_1, B_PIN_2 };
  const uint8_t _pwmpin[2] = { PWM_PIN_1, PWM_PIN_2 };
  const uint8_t _cspin[2] = { CS_PIN_1, CS_PIN_2 };
  const uint8_t _enpin[2] = { EN_PIN_1, EN_PIN_2 };
  uint8_t _mode;

  bool _validateSpeed(uint8_t speed);
  void _validateMode(uint8_t mode);

public:
  Monster(uint8_t mode);
  ~Monster();
  void stopMotor(uint8_t motor);
  void stop();
  void setSpeed(uint8_t motor, uint8_t speed);
  void forward(uint8_t speed);
  void backward(uint8_t speed);
  void driveRight(uint8_t speed);
  void driveLeft(uint8_t speed);
  void turnLeft(uint8_t speed);
  void turnRight(uint8_t speed);
  void driveMotor(uint8_t motor, uint8_t direction, uint8_t speed);
  uint8_t readCurrent(uint8_t motor);

};


#endif
