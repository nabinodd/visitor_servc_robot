
bool motInit(char s)
{   Serial.print(s);
    Serial.println(" Mot Init started");

    init_starting_time.tmr = millis();
    motRun(cw);
    while (!lmtS)
    {
        readLimits();
        runEncCount();
        if (init_starting_time.tmr + init_timeout < millis())
        {
            Serial.println("Motor init time Out");
            mot_err = true;
            return false;
        }
    }
    countt = 0;
    writeIntIntoEEPROM(1, countt);
    Serial.println("Mot init success");
    prepAck(ack_mot_init_reg,0);
    return true;
}

bool rotateToPos(int pos)
{
    Serial.print("Now at : ");
    Serial.print(countt);
    Serial.print(" Going to pos : ");
    Serial.println(pos);

    if (pos == 0)
    {
        if (motInit('C'))
            return true;
        else
            return false;
    }
    //figuring out direcction to rotate
    else if (countt < pos && pos < enc_max) //if current count is less then desired pos and pos not greater than enc_max
    {
        count_starting_time.tmr = millis();
        motRun(ccw);           //rotate motor CCW
        while (countt <= pos) //waiting for motor to reach the target pos
        {
            readLimits();
            runEncCount();
            if (count_starting_time.tmr + init_timeout < millis()) //if TIMEOUT return false
            {
                Serial.println("Rotating CW time out");
                mot_err = true;
                return false;
            }
        }
        motRun(stp);
        return true; //if success return true
    }
    else if (countt > pos && pos >= 0) //if current count is greater then desired pos and pos not smaller than 0
    {
        count_starting_time.tmr = millis();
        motRun(cw);
        while (countt >= pos)
        {
            readLimits();
            runEncCount();
            if (count_starting_time.tmr + init_timeout < millis())
            {
                Serial.println("Rotating CCW time out");
                mot_err = true;
                return false;
            }
        }
        motRun(stp);
        return true;
    }
    else if (countt == pos)
    {
        Serial.print("Already at : ");
        Serial.println(countt);
        motRun(stp);
        return true;
    }
    else
    {
        Serial.println("ERROR!!!");
        return false;
    }
}

void writeIntIntoEEPROM(int address, int number)
{
  EEPROM.update(address, number >> 8);
  EEPROM.update(address + 1, number & 0xFF);
}

int readIntFromEEPROM(int address)
{
  return (EEPROM.read(address) << 8) + EEPROM.read(address + 1);
}
