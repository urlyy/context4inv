int main(int x,int y,int z) {
  if ((x == y && y == 0 && z==0)){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      x++;y++;z-=2;
    }
    //@ assert(x == y && x >= 0 && x+y+z==0);
  }
  return 0;
}
