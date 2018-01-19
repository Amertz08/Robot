AB=arduino-builder
BOARD=arduino:avr:uno


ultra:
	$(AB) -hardware ${ARDUINO_HARDWARE_DIR} \
	-tools ${ARDUINO_TOOLS_DIR} \
	-fqbn $(BOARD) \
	-libraries ${ARDUINO_LIB_DIR} \
	-warnings all \
	$(shell pwd)/ultra.ino
