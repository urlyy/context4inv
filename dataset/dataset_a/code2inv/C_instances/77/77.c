int main() {
  // variable declarations
  int i;
  int x;
  int y;
  // pre-conditions
  i = 0;
  //@ assume(x >= 0)
  //@ assume(y >= 0)
  //@ assume(x >= y)
  // loop body
  int unknown1, unknown2;
  while (unknown1!=0) {
    if (i < y){
      i  = i + 1;
    }
  }
  // post-condition
  //@ assert((i < y)=>(i < x))
}
