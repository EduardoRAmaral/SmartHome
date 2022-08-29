/**
 * @file ArduinoUARTLib.cpp
 * @date 15/05/2022
 * @author Joaquim Ferrer Sagarra
 */

#include "ArduinoUARTLib.h"

Arduino_UART_Lib::Arduino_UART_Lib() {
	// TODO Auto-generated constructor stub
	snd_state = UART_IDLE;
	rcv_state = UART_IDLE;
	//linkSerial = nullptr;
}

//Arduino_UART_Lib::Arduino_UART_Lib(Stream * serial_connection) {
//	// TODO Auto-generated constructor stub
//	snd_state = UART_IDLE;
//	rcv_state = UART_IDLE;
//	linkSerial = serial_connection;
//}


Arduino_UART_Lib::~Arduino_UART_Lib() {
	// TODO Auto-generated destructor stub
}

bool Arduino_UART_Lib::run_rcv(message_code_t * code, char * data, int * data_len) {
	static int cont = 0;
	bool result = false;

	if (Serial.available())
	  {
		if (rcv_state == UART_IDLE){    //New header received
			act_message.header.char_header = Serial.read();

			if (act_message.header.df_header.len == 0){ //all message received
				rcv_state = UART_IDLE;
				data = nullptr;
				*data_len = 0;
				*code = act_message.header.df_header.code;
				return true;
			}
			else {						//Prepare to receive data on next frame
				reset_counters();
				rcv_counters.data_top = act_message.header.df_header.len;
				rcv_counters.time = millis();
				rcv_state = UART_RCVNG;
				return false;
			}
		}
		else {							//Continue receiving message
			if(millis() - rcv_counters.time >= UART_TIMEOUT){
				rcv_state = UART_IDLE;
				reset_counters();
				return false;
			} else {
				act_message.data[rcv_counters.data_it] = Serial.read();
				rcv_counters.data_it++;
				if(rcv_counters.data_it >= rcv_counters.data_top){
					memcpy(data,act_message.data,rcv_counters.data_it);
					*data_len = rcv_counters.data_it;
					*code = act_message.header.df_header.code;
					this->rcv_state = UART_IDLE;
					reset_counters();
					return true;
				}
			}
		 }
	  }
	return result;
}

bool Arduino_UART_Lib::send(bool success, void * data, int len) {
	bool result = true;
	message_t msg_to_send;
	if (len > MAX_DATA_LEN){
		result = false;
	} else {
		if(success){
			msg_to_send.header.df_header.code = (uint8_t) ACK;
		} else {
			msg_to_send.header.df_header.code = (uint8_t) NACK;
		}
		msg_to_send.header.df_header.len = (char)len;
		memcpy(msg_to_send.data,data,len);
		Serial.write((char *)&msg_to_send, len+1);
	}
	return result;
}

void Arduino_UART_Lib::reset_counters() {
	memset(&rcv_counters,0,sizeof(rcv_counters));
}

bool Arduino_UART_Lib::setup(int speed) {
	rcv_state = UART_IDLE;
	Serial.begin(speed);

	return true;
}
