int main() {
  // variable declarations
  int x;
  int y;
  // pre-conditions
  //@ assume(x >= 0)
  //@ assume(x <= 10)
  //@ assume(y <= 10)
  //@ assume(y >= 0)
  // loop body
  int unknown1, unknown2;
  while (unknown1!=0) {
    x  = x + 10;
    y  = y + 10;
    unknown1= unknown2;
  }
  // post-condition
  //@ assert((x >= 20)=>(y != 0))
}
