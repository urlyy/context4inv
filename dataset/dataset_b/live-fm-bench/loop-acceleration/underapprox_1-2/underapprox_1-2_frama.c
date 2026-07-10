int foo() {
  unsigned int x = 0;
  unsigned int y = 1;
  while (x < 6) {
    x++;
    y *= 2;
  }
  //@ assert(y % 3!=0);
  return 0;
}
