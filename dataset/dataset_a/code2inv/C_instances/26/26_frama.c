void fmain(int n) {
  // variable declarations
  int x;
  // pre-conditions
  x = n;
  // loop body
  while (x > 1) {
    x  = x - 1;
  }
  // post-condition
  //@ assert( (x!=1)==>(n<=0) );
}
