int main(int x,int y) {
  if ((x == y && y == 0)){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      x++;y++;
    }
    //@ assert(x == y && x >= 0);
  }
  
  return 0;
}
