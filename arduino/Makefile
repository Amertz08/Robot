AB=arduino-builder
BOARD=arduino:avr:uno
COMMAND=$(AB) -hardware ${ARDUINO_HARDWARE_DIR} \
	-tools ${ARDUINO_TOOLS_DIR} \
	-tools ${ARDUINO_BASE_DIR}/Java/tools-builder \
	-fqbn $(BOARD) \
	-libraries ${ARDUINO_LIB_DIR} \
	-warnings all

.PHONY: ultra

ultra:
	$(COMMAND) \
	-build-path $(shell pwd)/ultra/build \
	$(shell pwd)/ultra/ultra.ino

line:
	$(COMMAND) \
	-build-path $(shell pwd)/linefollower/build \
	$(shell pwd)/linefollower/MostBasicFollower.ino

clean:
	rm -rf ./*/build
	mkdir ./ultra/build ./linefollower/build
