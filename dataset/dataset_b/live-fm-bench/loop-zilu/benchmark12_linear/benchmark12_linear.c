int main(int x,int y,int t) {
  if (x!=y && y==t){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      if(x>0) y=y+x;
    }
    //@ assert(y>=t);
  }
  return 0;
}
