/*@ ensures \result >= 0 && \result <= 10; */
int unknown1();

/*@ ensures \result <= 10 && \result >= 0; */
int unknown3();

void fmain() {
  // variable declarations
  int x = unknown1();
  int y = unknown3();
  // loop body
  while (unknown()) {
    x  = x + 10;
    y  = y + 10;
  }
  // post-condition
  //@ assert((x >= 20)==>(y != 0));
}