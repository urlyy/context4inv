int foo(void) {
  unsigned int x = 1;
  while (unknown()) {
    x += 2;
  }
  //@ assert(x % 2==1);
  return 0;
}