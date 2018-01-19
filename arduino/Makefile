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

clean:
	rm -rf ./sensors/*/build
	mkdir ./sensors/ultra/build ./sensors/linefollower/build
