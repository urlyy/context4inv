int main(int x,int y) {
  if ((y == x)){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      x++;
      y++;
    }
    //@ assert(x == y);
  }
  return 0;
}
