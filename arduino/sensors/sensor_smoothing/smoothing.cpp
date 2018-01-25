#include "smoothing.h"

SMOOTHING::SMOOTHING(int numRead)
{
	numReadings = numRead;
	readings = new int[numReadings];
	readIndex = 0;
	total = 0;
	average = 0;
	for (int i = 0; i < numReadings; i++)
	{
		readings[i] = 0;
	}
}

SMOOTHING::~SMOOTHING()
{
	delete [] readings;
	readings = NULL;
}

int SMOOTHING::smooth(int newValue)
{
	int newAvg;
	total = total - readings[readIndex];
	readings[readIndex] = newValue;
	total = total + readings[readIndex];
	readIndex = readIndex + 1;

	if (readIndex >= numReadings)
	{
		readIndex = 0;
	}

	newAvg = total / numReadings;
	return newAvg;
}
