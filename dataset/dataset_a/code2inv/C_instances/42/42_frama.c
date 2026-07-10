/*@ ensures \result > 0; */
int unknown1();

void fmain() {
  // variable declarations
  int c;
  int n = unknown1();
  // pre-conditions
  c = 0;
  
  // loop body
  while (unknown()) {
    if ( unknown()) {
      if (c > n){
        c  = c + 1;
      }
    } else {
      if (c == n){
        c  = 1;
      }
    }
  }
  // post-condition
  //@ assert( (c < 0 && c > n)==>(c == n) );
}