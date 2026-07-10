/*@ ensures \result >= 0; */
int unknown1();

void fmain() {
  // variable declarations
  int n = unknown1();
  int x;
  // pre-conditions
  x = 0;
  
  // loop body
  while (x < n) {
    x  = x + 1;
  }
  // post-condition
  //@ assert(x == n);
}
