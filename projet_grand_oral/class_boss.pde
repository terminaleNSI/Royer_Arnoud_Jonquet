int nx= 100;
int ny=100;
int attx=100;
int atty=150;


class Boss{
PImage IBoss=loadImage("link.png");
  
Boss(PImage NBoss)
{
NBoss=IBoss;
}
  
void display()
{
  image(IBoss,nx,ny);
  IBoss.resize(100,100);
  image(IBoss,nx,ny);
  
}

void attack()
{
    circle(attx,atty,20);
    if(attx>800 || attx<0)
    {
      attx=nx;
      atty=ny+50;
    }
}

void up()
{
  if(keys[0]== true && y>0)
  {
  ny-=2;
  bossy-=2;
  atty-=2;
  }
}
void down()
{
  if(keys[1]== true && y<height-40)
  {
   ny+=2;
   bossy+=2;
   atty+=2;
  }
}
void right()
{
  if(keys[2]== true && x<width-40)
  {
    nx+=2;
    bossx+=2;
    attx+=2;
  }
}
void left()
{
  if(keys[3]== true && x>0)
  {
    nx-=2;
    bossx-=2;
    attx-=2;
  }
}

void move()
{
  attx+=10;
}
void xmove()
{
  attx-=10;
}
}
