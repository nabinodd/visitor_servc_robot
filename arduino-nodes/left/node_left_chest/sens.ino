void runEncCount()
{

  bool enc_dt_st = digitalRead(enc_pin);
  if (enc_dt_st != enc_last_dt)
  {
    runn = true;
    run_true_time = millis();
    if (mot_dir == cw)
    {
      if (countt > 0)
        countt--;
      new_enc_data = true;
    }
    else if (mot_dir == ccw)
    {
      countt++;
      new_enc_data = true;
    }
  }
  enc_last_dt = enc_dt_st;
}

void readLimits()
{
  lmtS = digitalRead(lmtS_pin);
  if (lmtS == true)
  {
    countt = 0;
    writeIntIntoEEPROM(1, countt);
  }
}

void runningDet()
{
  if (millis() > run_true_time + SAMPLE_TIME_RUN)
  {
    runn = false;
  }
}