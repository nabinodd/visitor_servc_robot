void runEncCount()
{

  bool enc_dt_st = digitalRead(enc_pin);
  if (enc_dt_st != enc_last_dt)
  {
    if (mot_dir == cw)
    {
      countt++;
      new_enc_data = true;
    }
    else if (mot_dir == ccw)
    {
      if (countt > 0)
        countt--;
      new_enc_data = true;
    }
  }
  enc_last_dt = enc_dt_st;
}

void readLimits()
{
  lmtS = digitalRead(lmtS_pin);
  lmtE = digitalRead(lmtE_pin);
  if (lmtS == true)
    countt = 0;

  else if (lmtE == true)
  {
    countt = enc_max;
    writeIntIntoEEPROM(1, countt);
  }
}