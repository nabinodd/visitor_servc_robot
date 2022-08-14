
void receiveEvent(int howMany)
{
    int c = 0;
    while (Wire.available() > 0)
    {
        buff[c] = Wire.read();
        c++;
    }
    new_i2c_data = true;
}

void prepAck(byte reg, int ack_int)
{
    itoa(ack_int, ack_bytes_array, 10);
    ack_reg = reg;
    ack_prep = true;
    commReqLine(true);
}

void requestEvent()
{
    if (ack_prep)
    {
        Wire.write(ack_reg);
        Wire.write(ack_bytes_array, 3);
    }
    else
    {
        itoa(countt, ack_enc_pos_array, 10);
        Wire.write(ack_enc_pos_reg);
        Wire.write(ack_enc_pos_array, 3);
    }
    ack_prep = false;
    flushAckArr();
    commReqLine(false);
}

void displayFullMsg()
{
    byte reg_byte = buff[0];
    byte cmd_msg_length = buff[1] + 1;
    Serial.print("Data : ");
    for (int i = 0; i <= cmd_msg_length; i++)
    {
        Serial.print((buff[i]));
        Serial.print(" ");
    }
    Serial.println("");
}

int getPos()
{
    byte pos[4] = {buff[2], buff[3], buff[4], '\0'};
    return (atoi(pos));
}

int commReqLine(bool sts)
{
    if (sts)
        digitalWrite(comm_req_pin, LOW); //set comm req line
    else if (!sts)
        digitalWrite(comm_req_pin, HIGH); //release comm line
}

void flushBuff()
{
    for (int i = 0; i <= 20; i++)
        buff[i] = 0;
}

void flushAckArr()
{
    for (int i = 0; i <= 3; i++)
        ack_bytes_array[i] = 0;
}