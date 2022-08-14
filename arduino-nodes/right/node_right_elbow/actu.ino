void motRun(dirs mot_cmd_dir)
{
    if (mot_cmd_dir == cw)
    {
        digitalWrite(in1_pin, HIGH);
        digitalWrite(in2_pin, LOW);
        analogWrite(pwm_pin, mot_pwr);
        mot_dir = cw;
    }
    else if (mot_cmd_dir == ccw)
    {
        if (countt >= enc_max)
            return;
        digitalWrite(in1_pin, LOW);
        digitalWrite(in2_pin, HIGH);
        analogWrite(pwm_pin, mot_pwr);
        mot_dir = ccw;
    }
    else if (mot_cmd_dir == stp)
    {
        digitalWrite(in1_pin, LOW);
        digitalWrite(in2_pin, LOW);
        digitalWrite(pwm_pin, LOW);
        mot_dir = stp;
    }
}
