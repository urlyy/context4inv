int foo() {
  unsigned int x = 0;
  while (x < 1025) {
    if (x < 1024) {
      x++;
    } else {
      x += 2;
    }
  }
  //@ assert(x % 2==0);
  return 0;
}
