int main(void) {
  unsigned int x = 1;
  int unknown1, unknown2;
  while (unknown1!=0) {
    x += 2;
    unknown1=unknown2;
  }
  //@ assert(x % 2==1);
  return 0;
}
