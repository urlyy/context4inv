/*@ ensures \result >= 0; */
int unknown1();

void fmain() {
  // variable declarations
  int n = unknown1();
  int x;
  int y;
  // pre-conditions
  
  x = n;
  y = 0;
  // loop body
  while (x > 0) {
    y  = y + 1;
    x  = x - 1;
  }
  // post-condition
  //@ assert(y == n);
}
