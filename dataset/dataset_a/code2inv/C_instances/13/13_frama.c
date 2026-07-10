/*@ ensures \result >= 0 && \result <= 2; */
int unknown1();

/*@ ensures \result <= 2 && \result >= 0; */
int unknown3();

void fmain() {
  // variable declarations
  int x = unknown1();
  int y = unknown3();
  int z1;
  int z2;
  int z3;
  // loop body
  while (unknown()) {
    x  = x + 2;
    y  = y + 2;
  }
  // post-condition
  //@ assert( (x == 4)==>(y != 0) );
}