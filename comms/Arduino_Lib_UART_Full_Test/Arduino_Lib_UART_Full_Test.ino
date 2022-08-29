#include "Arduino.h"
#include "ArduinoUARTLib.h"


#define CODE_IN_TEST		SET_LIGHTS_OFF

Arduino_UART_Lib uart;
int len;
char data[16];
message_code_t rcv_code;
int new_len = 1;
char new_in[16];


bool correct_in(char * data, int len){
	bool result = true;
	for (int i = 0; i < len; i++){
		if(data[i] != new_in[1]){
			result = false;
			break;
		}
	}
	return result;
}

bool check_verification_code(message_code_t code, char * data, int len){
	bool result = true;
	if(len != new_len or not correct_in(data,len)){
		result = false;
	}
	return result;
}

void setup()
{
	uart = Arduino_UART_Lib(/*&Serial*/);
	uart.setup(9600);

	new_in[0] = 0x01;
}

void loop()
{
	//This is an example of how to perform communication with the lib.
	bool run_machine = uart.run_rcv(&rcv_code, data, &len);
	if(run_machine){
		//Doing something stupid to verify data
		if(check_verification_code(rcv_code,data,len)){
			//Responding ACKOWLEDGE (OK) with back validation code
			uart.send(true, nullptr, 0);
		} else {
			//Repsonding NOT ACKNOWLEDGE (NOT OK) with no data
			uart.send(false, nullptr, 0);
		}
		new_in[new_len] = 0x01;
		if(++new_len > 16){
			new_len = 1;
		}

	}
}
