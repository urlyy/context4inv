int main(int x,int y) {
  if ((x*y>=0)){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      if(x==0) {
        if (y>0) x++;
        else x--;
      } 
      if(x>0) y++;
      else x--;
    }
    //@ assert(x*y>=0);
  }
  return 0;
}
