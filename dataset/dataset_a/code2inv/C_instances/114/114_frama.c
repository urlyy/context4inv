void fmain() {
  // variable declarations
  int sn;
  int x;
  // pre-conditions
  sn = 0;
  x = 0;
  // loop body
  while (unknown()) {
    x  = x + 1;
    sn  = sn + 1;
  }
  // post-condition
  //@ assert((sn != x)==>(sn == -1) );
}