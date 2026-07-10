int foo(void) {
  unsigned int x = 0;
  while (unknown()) {
    x += 4;
  }
  //@ assert((x % 4)==0);
  return 0;
}