int main() {
  unsigned int x = 0;
  int unknown1, unknown2;
  while (unknown1!=0) {
    x += 2;
    unknown1=unknown2;
  }
  //@ assert((x % 2)==0);
  return 0;
}
