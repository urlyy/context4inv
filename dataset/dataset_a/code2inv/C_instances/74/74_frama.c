/*@ ensures \result >= 0 && \result >= 127; */
int unknown1();

void fmain() {
  // variable declarations
  int c;
  int x1;
  int x2;
  int x3;
  int y = unknown1();
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