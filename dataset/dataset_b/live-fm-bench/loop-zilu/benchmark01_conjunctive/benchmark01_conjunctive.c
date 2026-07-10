int main(int x,int y) {
  if (x==1 && y==1){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      x=x+y;
      y=x;
    }
    //@ assert(y>=1);
  }
  return 0;
}
