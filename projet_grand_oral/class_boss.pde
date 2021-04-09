int nx= 100;
int ny=100;
int attx=100;
int atty=100;
int time=0;
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
  if (millis() > time + 100)
  {
    circle(attx,atty,20);
    for(int i=0;i<20;i+=1)
    {
    circle(attx,atty,20);
    move();
    circle(attx,atty,20);
    }
  }
    time=millis();;
}

void up()
{
  if(keys[0]== true && y>0)
  {
  ny-=2;
  bossy-=2;
  }
}
void down()
{
  if(keys[1]== true && y<height-40)
  {
   ny+=2;
   bossy+=2;
  }
}
void right()
{
  if(keys[2]== true && x<width-40)
  {
    nx+=2;
    bossx+=2;
  }
}
void left()
{
  if(keys[3]== true && x>0)
  {
    nx-=2;
    bossx-=2;
  }
}

void move()
{
  attx+=10;
}
}
