void fmain(int n) {
  // variable declarations
  int v1;
  int v2;
  int v3;
  int x;
  // pre-conditions
  x = n;
  // loop body
  while (x > 0) {
    x  = x - 1;
  }
  // post-condition
  //@ assert((n >= 0)==> (x == 0));
}
