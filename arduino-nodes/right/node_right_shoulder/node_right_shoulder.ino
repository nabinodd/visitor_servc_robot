
#include <Wire.h>
#include <stdlib.h>
#include <EEPROM.h>
#define SAMPLE_TIME_RUN 100
/**************************************/
#define ADDR 13 //I2C address
String idString = "node-RightShoulder-A";
/**************************************/
const int enc_pin = 6;
const int pwm_pin = 3;
const int in1_pin = 9;
const int in2_pin = 8;
const int lmtS_pin = 4;
const int comm_req_pin = 7;
/**************************************/
const byte cmd_mot_pos_reg = 1;
const byte cmd_mot_ccw_reg = 2;
const byte cmd_mot_stop_reg = 3;
const byte cmd_mot_init_reg = 4;
const byte cmd_ack_release_reg = 55;
const byte cmd_reset_cntlr = 88;
const byte req_reg = 22;

const byte ack_mot_pos_reg = 11;
const byte ack_mot_init_reg = 44;
const byte ack_mot_err_reg = 77;
const byte ack_enc_pos_reg = 33;

/**************************************/
byte buff[20];

char ack_bytes_array[3];
byte ack_reg = 0;
bool ack_prep = true;
bool new_i2c_data = false;

bool new_enc_data = false;
bool enc_dt_st = false;
bool enc_last_dt = false;
byte ack_enc_pos_array[] = {0, 0, 0};

int countt = 0;
int enc_max = 25;
int enc_normal = 10;

bool lmtS = false;
bool lmtE = false;

byte mot_st = 0;
bool mot_err = false;
bool mot_stop = false;
byte mot_pwr_cw = 50;
byte mot_pwr_ccw = 160;

/********************************************/
byte starting_up_pwr = 15;
byte starting_down_pwr = 15;

byte max_up_pwr = 180;
byte max_down_pwr = 65;

byte up_power = starting_up_pwr;
byte down_power = starting_down_pwr;
bool runn = false;
unsigned long int run_true_time = 0;
/********************************************/

const int init_timeout = 10000;
const int loop_reading_timeout = 1000;

enum dirs
{
  none,
  cw,
  ccw,
  stp
};

dirs mot_dir = none;
dirs mot_cmd_dir = none;

struct pos_cmd_sts
{
  bool init = false;
  bool rcv = false;
  bool exec = false;
} pos_cmd;

struct timez
{
  unsigned long int tmr = 0;
} init_starting_time, count_starting_time, rotation_end_time;

void (*resetFunc)(void) = 0; //declare reset function at address 0

void setup()
{
  pinMode(enc_pin, INPUT);
  pinMode(pwm_pin, OUTPUT);
  pinMode(in1_pin, OUTPUT);
  pinMode(in2_pin, OUTPUT);
  pinMode(lmtS_pin, INPUT);
  pinMode(comm_req_pin, OUTPUT);
  digitalWrite(comm_req_pin, HIGH);

  Wire.begin(ADDR);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);

  Serial.begin(115200);
  Serial.print("\n\n");
  Serial.println(idString);

  countt = readIntFromEEPROM(1);
  Serial.print("\nBooting with value : ");
  Serial.println(countt);
}

void loop()
{

  if (new_i2c_data)
  {
    byte cmd_reg_byte = buff[0];

    switch (cmd_reg_byte)
    {

    case (req_reg):
      break;

    case (cmd_mot_pos_reg):
      if (rotateToPos(getPos()))
      {
        Serial.println("Rotation complete");
        writeIntIntoEEPROM(1, countt);
        prepAck(11, countt);
      }
      else
        prepAck(77, countt);

      break;

    case (cmd_mot_init_reg):
      motInit('L');
      break;

    case (cmd_ack_release_reg):
      commReqLine(false);
      break;

    case (cmd_reset_cntlr):
      Serial.println("Going to reset");
      delay(1000);
      resetFunc();
      break;
    }

    new_i2c_data = false;
    flushBuff();
  }
  else if (millis() < rotation_end_time.tmr + loop_reading_timeout)
  {
    readLimits();
    runEncCount();
  }
}
