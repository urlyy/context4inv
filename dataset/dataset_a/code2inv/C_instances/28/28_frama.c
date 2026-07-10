void fmain(int n) {
  // variable declarations
  int x;
  // pre-conditions
  x = n;
  // loop body
  while (x > 0) {
    x  = x - 1;
  }
  // post-condition
  //@ assert((x != 0)==> (n < 0));
}
