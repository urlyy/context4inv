int main() {
  // variable declarations
  int c;
  // pre-conditions
  c = 0;
  // loop body
  int unknown1, unknown2, unknown3, unknown4;
  while (unknown1!=0) {
    if ( unknown3!=0 ) {
      if ( c != 4 ){
        c  = c + 1;
      }
    } else {
      if ( c == 4 ){
        c  = 1;
      }
    }
    unknown1 = unknown2;
    unknown3 = unknown4;
  }
  // post-condition
  //@ assert( (c < 0 && c > 4)=>(c == 4) )
