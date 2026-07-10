int main() {
  // variable declarations
  int x;
  int y;
  int z1;
  int z2;
  int z3;
  int unknown1, unknown2;
  // pre-conditions
  //@ assume((x >= 0))
  //@ assume((x <= 10))
  //@ assume((y <= 10))
  //@ assume((y >= 0))
  // loop body
  while (unknown1!=0) {
    x  = x + 10;
    y  = y + 10;
    unknown1 = unknown2;
  }
  // post-condition
  //@ assert( (x == 20)=>(y != 0) )
}
