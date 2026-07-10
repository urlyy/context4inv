int main(int y) {
  // variable declarations
  int c;
  int z;
  // pre-conditions
  c = 0;
  //@ assume((y >= 0))
  //@ assume((y >= 127))
  z = 36 * y;
  // loop body
  int unknown1, unknown2;
  while (unknown1!=0) {
    if (c < 36){
      z  = z + 1;
      c  = c + 1;
    }
    unknown1=unknown2;
  }
  // post-condition
  //@ assert((c < 36)=>(z >= 0))
}
