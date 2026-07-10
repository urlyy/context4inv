void fmain() {
  // variable declarations
  int c;
  // pre-conditions
  c = 0;
  // loop body
  while (unknown()) {
    if ( unknown() ) {
      if ( c != 4 ){
        c  = c + 1;
      }
    } else {
      if ( c == 4 ){
        c  = 1;
      }
    }
  }
  // post-condition
  //@ assert( (c != 4)==>(c >= 0) );
}