void motRun(dirs mot_cmd_dir)
{
    if (mot_cmd_dir == cw)
    {
        digitalWrite(in1_pin, HIGH);
        digitalWrite(in2_pin, LOW);
        digitalWrite(pwm_pin, HIGH);
        mot_dir = cw;
    }
    else if (mot_cmd_dir == ccw)
    {
        digitalWrite(in1_pin, LOW);
        digitalWrite(in2_pin, HIGH);
        digitalWrite(pwm_pin, HIGH);
        mot_dir = ccw;
    }
    else if (mot_cmd_dir == stp)
    {
        if (mot_dir == cw)
        {
            digitalWrite(in1_pin, LOW);
            digitalWrite(in2_pin, HIGH);
            analogWrite(pwm_pin, 50);
            delay(50);
        }
        else if (mot_dir == ccw)
        {
            digitalWrite(in1_pin, HIGH);
            digitalWrite(in2_pin, LOW);
            analogWrite(pwm_pin, 50);
            delay(50);
        }
        digitalWrite(in1_pin, LOW);
        digitalWrite(in2_pin, LOW);
        digitalWrite(pwm_pin, LOW);
        mot_dir = stp;
    }
}
