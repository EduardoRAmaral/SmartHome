/**
 * @file ArduinoUARTLib.h
 * @date 15/05/2022
 * @author Joaquim Ferrer Sagarra
 */

#ifndef ARDUINOUARTLIB_H_
#define ARDUINOUARTLIB_H_

#define SND_BUFFER_LEN 		256
#define MAX_DATA_LEN 		16		//In Bytes. If it changes header of messages must change.
#define UART_DATAGRAM_LEN	8
#define	UART_TIMEOUT		500		//Serial Timeout in millis.

//#include "SoftwareSerial.h"
#include "Arduino.h"


typedef enum {
	UART_IDLE,
	UART_RCVNG,
} UART_state_t;

typedef enum {
	ACK,
	NACK,
	LUM,
	TMP,
	SET_LIGHTS_ON,
	SET_LIGHTS_OFF,
	GET_LIGHTS,
	SET_AUTOMODE,
	GET_AUTOMODE,
	OCCUPIED
} message_code_t;

//typedef enum {
//	OK,
//	TIMEOUT,
//	RECEIVING,
//	RECEIVED,
//	IDLE,
//	ERROR
//} com_state_t;


//Message datagram definitions.
typedef struct {
	message_code_t code 	: 4;
	int len					: 4; //Max 16 bytes datalen
} message_defined_header_t;

typedef union{
	message_defined_header_t df_header;
	char char_header;
} message_header_t;

typedef struct {
	message_header_t header;
	//char index;					//Number of datagram.
	char data[MAX_DATA_LEN];
} message_t;

typedef struct {
	char 					data_it;   	//Bytes received
	char 					data_top;	//Bytes to receive
	unsigned long			time;		//For timeout
} rcv_counters_t;

class Arduino_UART_Lib {

private:
	char send_buffer[SND_BUFFER_LEN];   //circular buffers
	UART_state_t snd_state;
	UART_state_t rcv_state;

	rcv_counters_t rcv_counters;

	message_t act_message;

	//HardwareSerial * linkSerial;


	void reset_counters();

public:
	Arduino_UART_Lib();
	//Arduino_UART_Lib(Stream * serial_connection);
	virtual ~Arduino_UART_Lib();

	bool run_rcv(message_code_t * code, char * data, int * data_len);
	bool send(bool success, void * data, int len);

	bool setup(int speed);
};

#endif /* ARDUINOUARTLIB_H_ */
