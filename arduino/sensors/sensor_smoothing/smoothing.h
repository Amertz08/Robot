#ifndef SMOOTHING_H
#define SMOOTHING_H

#include <Arduino.h>

class SMOOTHING{
public:
	SMOOTHING(int numRead);
	~SMOOTHING();
	//void setNumReadings();
	int smooth(int newValue);
private:
	int numReadings;
	int* readings;
	int readIndex;
	int total;
	int average;
};

#endif