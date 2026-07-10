int main() {
  // variable declarations
  int lock;
  int x;
  int y;
  // pre-conditions
  y = x + 1;
  lock = 0;
  // loop body
  int unknown1, unknown2;
  while (x != y) {
    if ( unknown1!=0 ) {
      lock = 1;
      x = y;
    } else {
      lock  = 0;
      x = y;
      y = y + 1;
    }
    unknown1 = unknown2;
  }
  // post-condition
  //@ assert(lock == 1)
}
