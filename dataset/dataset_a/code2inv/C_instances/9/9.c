int main() {
  // variable declarations
  int x;
  int y;
  // pre-conditions
  //@ assume(x >= 0)
  //@ assume(x <= 2)
  //@ assume(y <= 2)
  //@ assume(y >= 0)
  // loop body
  int unknown1, unknown2;
  while (unknown1!=0) {
    x  = x + 2;
    y  = y + 2;
    unknown1= unknown2;
  }
  // post-condition
  //@ assert((x == 4)=> (y != 0))
}
