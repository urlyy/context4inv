void fmain() {
  // variable declarations
  int n;
  int v1;
  int v2;
  int v3;
  int x;
  // pre-conditions
  x = 0;
  // loop body
  while (x < n) {
    x  = x + 1;
  }
  // post-condition
  //@ assert((x != n)==>(n < 0));
}
