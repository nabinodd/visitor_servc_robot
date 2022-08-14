void motRun(dirs mot_cmd_dir)
{
    if (mot_cmd_dir == cw) //going down
    {
        digitalWrite(in1_pin, HIGH);
        digitalWrite(in2_pin, LOW);
        if (countt < 7)
            analogWrite(pwm_pin, down_power-10);
        else
            analogWrite(pwm_pin, down_power);
        mot_dir = cw;
    }
    else if (mot_cmd_dir == ccw) //going up
    {
        if (countt >= enc_max)
            return;
        digitalWrite(in1_pin, LOW);
        digitalWrite(in2_pin, HIGH);
        analogWrite(pwm_pin, up_power);

        mot_dir = ccw;
    }
    else if (mot_cmd_dir == stp)
    {
        digitalWrite(in1_pin, LOW);
        digitalWrite(in2_pin, LOW);
        digitalWrite(pwm_pin, LOW);
        up_power = starting_up_pwr;
        down_power = starting_down_pwr;
        mot_dir = stp;
    }
}
void upPowerController()
{
    if (runn == false)
    {
        if (up_power < max_up_pwr)
        {
            up_power++;
            // Serial.println(up_power);
            delay(5);
        }
    }
}

void downPowerController()
{
    if (runn == false)
    {
        if (down_power < max_down_pwr)
        {
            down_power++;
            // Serial.println(down_power);
            delay(20);
        }
    }
}
