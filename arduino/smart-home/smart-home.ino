/**
 * @file smart-home.ino
 *
 * @author Francisco Spínola
 */

#include <ArduinoUARTLib.h>

// PINS DEFINITION
#define temperaturePin A0
#define lightPin A1
#define echo 6
#define trig 5
#define ITER 100
#define LAST_CHANGE_TIMEOUT 5000
#define OCCUPIED_TIMEOUT 1000

Arduino_UART_Lib uart;
int len;
char data[16];
message_code_t rcv_code;
long int divs[] = {1, 2, 3, 4, 5};
long int pins[] = {12, 11, 10, 9, 8};
long int num_divs = 5;
bool autosystem;
long int prev_lum = 0;
bool light_status;
unsigned long auto_last_light_change;
long int mov_learn_counter;
long int mov_learn_vals[1000];
bool mov_learning;
long duration;
long int distance;
long average;
bool occupied;
bool flag;
unsigned long int light_threshold;
long int occ_time;

void all_lights_on() {
  for (long int l = 0; l < num_divs; l++) {
    digitalWrite(pins[l], HIGH);
  }
  light_status = true;
  auto_last_light_change = millis();
}

void all_lights_off() {
  for (int l = 0; l < num_divs; l++) {
    digitalWrite(pins[l], LOW);
  }
  light_status = false;
  auto_last_light_change = millis();
}

void setup() {
  uart = Arduino_UART_Lib();
  uart.setup(9600);
  autosystem = true;
  light_status = false;
  auto_last_light_change = 0;
  light_threshold = 500;
  occ_time = 0;

  // PINS
  pinMode(echo, INPUT);
  pinMode(trig, OUTPUT);
  for (int p = 0; p < num_divs; p++) {
    pinMode(pins[p], OUTPUT);
  }

  mov_learn_counter = 0;
  mov_learning = true;

  while (mov_learning) {
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);
    duration = pulseIn(echo, HIGH);
    distance = duration * 0.034 / 2; //cm
    mov_learn_vals[mov_learn_counter++] = distance;
    if (mov_learn_counter >= ITER) {
      mov_learning = false;
    }
  }

  // Learn average distance to door
  average = 0;
  for (int i = 0; i < ITER; i++) {
    average += mov_learn_vals[i];
  }
  average /= ITER;

  occupied = false;
  flag = false;
}

void loop() {
  // LIGHT
  long int lightreading = analogRead(lightPin);

  // MOTION
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = duration * 0.034 / 2; //cm

  // TEMPERATURE
  long int tempreading = analogRead(temperaturePin);
  float voltage = tempreading * (5000 / 1024.0);
  float temperature = (voltage - 500) / 10;


  //Presence

  if(occ_time == 0 or millis() - occ_time > OCCUPIED_TIMEOUT){
	  occ_time = 0;
	  if (distance  >= average - 10) {
		  flag = false;
	  }
	  if (distance < average - 10) {
		  if (!flag) {
			  occupied = !occupied;
			  //Serial.println("occ");
			  occ_time = millis();
			  flag = true;
		  }
	  }
  }

  if (autosystem) {
    if (millis() - auto_last_light_change > LAST_CHANGE_TIMEOUT) {
      if (lightreading - prev_lum > 5 || lightreading - prev_lum < -5) {
        if (!light_status && lightreading < light_threshold && occupied) {
          all_lights_on();
        } else if ((light_status && lightreading > light_threshold) || (!occupied && light_status)) {
          all_lights_off();
        }
      }
    }
  }

  if(uart.run_rcv(&rcv_code, data, &len)) {
    switch (rcv_code) {
      long int recvd;
      int i;

      case LUM: {
        if (len > 0) {
          long int threshold = *(long int*) data;  //Going to receive one int so 4 bytes
          if (threshold >= 0 && threshold <= 1000) {
            light_threshold = threshold;
            uart.send(true, (char *) &light_threshold, sizeof(light_threshold));
            break;
          } else {
          	uart.send(false, NULL, 0);
          	break;
          }
        } else {
          uart.send(true, (char *) &lightreading, sizeof(lightreading));
        }
        break;
      }
      case TMP: {
        uart.send(true, (char *) &temperature, sizeof(temperature));
        break;
      }
      case SET_LIGHTS_ON: {							//0, 4 and 5 not working
        recvd = (long int) data[0];
        if (recvd == 0) {
          for (int i = 0; i < num_divs; i++) {
            digitalWrite(pins[i], HIGH);
            //light_status = true;
          }
          uart.send(true, NULL, 0);
          break;
        } else {
          i = 0;
          while (i < num_divs && divs[i] != NULL && divs[i] != recvd) { i++; }
          if (i == num_divs) {
            uart.send(false, NULL, 0);
          } else {
            digitalWrite(pins[i], HIGH);
            uart.send(true, NULL, 0);
          }
        }
        break;
      }
      case SET_LIGHTS_OFF: {
        recvd = (long int) data[0];
        if (recvd == 0) {
          for (int i = 0; i < num_divs; i++) {
            digitalWrite(pins[i], LOW); 
            //light_status = false;
          }
          uart.send(true, NULL, 0);
        } else {
          i = 0;
          while (i < num_divs && divs[i] != NULL && divs[i] != recvd) { i++; }
          if (i == num_divs) {
            uart.send(false, NULL, 0);
          } else {
            digitalWrite(pins[i], LOW);
            uart.send(true, NULL, 0);
          }
        }
        break;
      }
      case GET_LIGHTS: {
        recvd = (long int) data[0];
        i = 0;
        if (recvd == 0) {
          char vals[5];
          for (int v = 0; v < num_divs; v++) {
            vals[v] = digitalRead(pins[v]) == HIGH ? 0x1 : 0x0;
          }
          uart.send(true, vals, sizeof(vals));
        } else {
          while (i < num_divs && divs[i] != NULL && divs[i] != recvd) { i++; }
          if (i == num_divs) {
            uart.send(false, NULL, 0);
          } else {
            char val = digitalRead(pins[i]) == HIGH ? 0x1 : 0x0;
            uart.send(true, &val, sizeof(val));
          }
        }
        
        break;
      }
      case SET_AUTOMODE: {
        long int val = (long int) data[0];
        if (val == 0) {
          autosystem = false;
          uart.send(true, NULL, 0);
        } else if (val == 1) {
          autosystem = true;
          prev_lum = 0;
          uart.send(true, NULL, 0);
        } else {
          long int ret = -1;
          uart.send(false, NULL, 0);
        }
        break;
      }
      case GET_AUTOMODE: {
        uart.send(true, &autosystem, sizeof(autosystem));
        break;
      }
      case OCCUPIED: {
        uart.send(true, &occupied, sizeof(occupied));
        break;
      }
      default: {
    	int code_in = rcv_code;
        uart.send(false, &rcv_code, sizeof(rcv_code));
        break;
      }
    }
  }
}
