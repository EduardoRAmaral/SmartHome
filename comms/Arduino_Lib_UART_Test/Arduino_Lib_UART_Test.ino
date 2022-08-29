#include "Arduino.h"
#include "ArduinoUARTLib.h"

#define VERIFICATION_CODE 	0x30403040
#define CODE_IN_TEST		SET_LIGHTS_OFF

Arduino_UART_Lib uart;
int len;
char data[16];
message_code_t rcv_code;
long int verification_code = VERIFICATION_CODE;


bool check_verification_code(message_code_t code, char * data, int len){
	if(len != sizeof(verification_code) or code != CODE_IN_TEST){
		return false;
	}
	return *(long int*)data == verification_code; //Treating data as int.
}

void setup()
{
	uart = Arduino_UART_Lib(/*&Serial*/);
	uart.setup(9600);
}

void loop()
{
	//This is an example of how to perform communication with the lib.
	bool run_machine = uart.run_rcv(&rcv_code, data, &len); 	//Should be called every iteration. Results are ok when result is true
	if(run_machine){
		//Doing something stupid to verify data
		if(check_verification_code(rcv_code,data,len)){
			//Responding ACKOWLEDGE (OK) with back validation code
			long int new_code = verification_code ^ 0x80808080;
			uart.send(true, &new_code, 4);
		} else {
			//Repsonding NOT ACKNOWLEDGE (NOT OK) with no data
			uart.send(false, nullptr, 0);
		}
	}
}

