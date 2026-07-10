void fmain() {
  // variable declarations
  int i;
  int n = unknown1();
  int x;
  int y;
  // pre-conditions
  i = 0;
  x = 0;
  y = 0;
  // loop body
  while (i < n) {
    i  = i + 1;
    if ( unknown() ) {
      x  = x + 1;
      y  = y + 2;
    } else {
      x  = x + 2;
      y  = y + 1;
    }
  }
  // post-condition
  //@ assert( 3 * n == x + y );
}