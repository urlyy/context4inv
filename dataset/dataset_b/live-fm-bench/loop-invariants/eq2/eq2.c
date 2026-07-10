int main(int w) {
  int x = w;
  int y = w + 1;
  int z = x + 1;
  int unknown1, unknown2;
  while (unknown1!=0) {
    unknown1=unknown2;
    y++;
    z++;
  }
  //@ assert(y == z);
  return 0;
}
