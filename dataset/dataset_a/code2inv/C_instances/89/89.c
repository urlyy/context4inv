int main() {
  // variable declarations
  int lock;
  int v1;
  int v2;
  int v3;
  int x;
  int y;
  // pre-conditions
  x = y;
  lock = 1;
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
