static boolean[] keys=new boolean[5];
int linkx=25;
int linky=25;
int bossx=150;
int bossy=150;

void setup()
{
Boss boss= new Boss(loadImage("link.png"));
frameRate(100);
size(800,600);
background(0);
for(int i =0;i<3;i+=1);
}
void draw()
{
  link Nlink= new link(loadImage("link.png"));
  Boss boss= new Boss(loadImage("link.png"));
  background(0);
  Nlink.affichage();
  boss.display();
  boss.attack();
  stroke(255,0,0);
  line(linkx,linky,bossx,bossy);
  if(keyPressed==true)
  {
  if(keys[0]==true)
    Nlink.up();
    boss.up();
  if(keys[1]==true)
    Nlink.down();
    boss.down();
  if(keys[2]==true)
    Nlink.right();
    boss.right();
  if(keys[3]==true)
    Nlink.left();
    boss.left();
  
  }
  //println(x,y,linkx,linky,bossx,bossy);
}
void keyPressed(){
  if(key=='z')
    keys[0]= true;
  if(key=='s')
    keys[1]= true;
  if(key=='d')
    keys[2]= true;
  if(key=='q')
    keys[3]= true;
  }


void keyReleased()
{
  if(key=='z')
    keys[0]= false;
  if(key=='s')
    keys[1]= false;
  if(key=='d')
    keys[2]= false;
  if(key=='q')
    keys[3]= false;
}
