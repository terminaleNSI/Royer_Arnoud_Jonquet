int x = 0;
int y = 0;
long nowpress=1000;
class link{
PImage Ilink=loadImage("link.png");
  
link(PImage Nlink)
{
Nlink=Ilink;
}
  
void affichage()
{
  image(Ilink,x,y);
}
void up()
{
  if(keys[0]== true && y>0) 
   {
    y-=5;
    linky-=5;
   }
}
void down()
{
  if(keys[1]== true && y<height-40)
  {
    y+=5;
    linky+=5;
  }
}
void right()
{
  if(keys[2]== true && x<width-40)
  {
  x+=5;
  linkx+=5;
  }
}
void left()
{
  if(keys[3]== true && x>0)
  {
  x-=5;
  linkx-=5;
  }
}
}
