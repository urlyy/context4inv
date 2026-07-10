int main() {
  // variable declarations
  int c;
  int n;
  // pre-conditions
  c = 0;
  //@ assume(n > 0)
  // loop body
  int unknown1, unknown2, unknown3, unknown4;
  while (unknown1!=0) {
    if ( unknown3!=0 ) {
      if (c > n){
        c  = c + 1;
      }
    } else {
      if (c == n){
        c  = 1;
      }
    }
    unknown1 = unknown2;
    unknown3 = unknown4;
  }
  // post-condition
  //@ assert( (c != n)=>(c <= n) )
}
