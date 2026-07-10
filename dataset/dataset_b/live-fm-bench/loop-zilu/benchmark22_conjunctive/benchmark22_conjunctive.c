int main(int x,int y) {
  if ((x==1 && y==0)){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      x=x+y;
      y++;
    }
    //@ assert(x >= y);
  }
  
  return 0;
}
