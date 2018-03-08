GPP=g++ -g -Wall -std=c++11
BOARD=arduino:avr:uno
ARD_LIB=$ARDUINO_BASE_DIR/Java/hardware/arduino/avr/cores/arduino
COMMAND=arduino-builder -hardware ${ARDUINO_HARDWARE_DIR} \
	-tools ${ARDUINO_TOOLS_DIR} \
	-tools ${ARDUINO_BASE_DIR}/Java/tools-builder \
	-fqbn $(BOARD) \
	-libraries ${ARDUINO_LIB_DIR} \
	-warnings all

.PHONY: ultra

ultra:
	$(COMMAND) \
	-build-path $(shell pwd)/sensors/ultra/build \
	$(shell pwd)/sensors/ultra/ultra.ino

line:
	$(COMMAND) \
	-build-path $(shell pwd)/sensors/linefollower/build \
	$(shell pwd)/sensors/linefollower/MostBasicFollower.ino

monster:
	$(COMMAND) \
	-build-path $(shell pwd)/drive/MonsterExp/build \
	$(shell pwd)/drive/MonsterExp/Monster.ino

Monster.o:
	$(GPP) -c $(shell pwd)/drive/Monster/Monster.cpp \
	-l $ARD_LIB \
	-o $(shell pwd)/drive/Monster/build/Monster.o

clean:
	rm -rf ./sensors/*/build ./drive/*/build
	mkdir \
	./sensors/ultra/build \
	./sensors/linefollower/build \
	./drive/MonsterExp/build \
	./drive/Monster/build
