/*@ ensures \result >= 0 && \result >= 127; */
int unknown1();

void fmain(int y) {
  y = unknown1();
  // variable declarations
  int c;
  int z;
  // pre-conditions
  c = 0;
  z = 36 * y;
  // loop body
  while (unknown()) {
    if (c < 36){
      z  = z + 1;
      c  = c + 1;
    }
  }
  // post-condition
  //@ assert((c < 36)==>(z >= 0));
}