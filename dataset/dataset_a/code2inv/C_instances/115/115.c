int main() {
  // variable declarations
  int sn;
  int x;
  // pre-conditions
  sn = 0;
  x = 0;
  // loop body
  int unknown1, unknown2;
  while (unknown1!=0) {
    x  = x + 1;
    sn  = sn + 1;
    unknown1 = unknown2;
  }
  // post-condition
  //@ assert((sn != -1)=>(sn == x) )
}
