int main(void) {
  unsigned int x = 0;
  int unknown1, unknown2;
  while (unknown1!=0) {
    x += 4;
    unknown1=unknown2;
  }
  //@ assert((x % 4)==0);
  return 0;
}
