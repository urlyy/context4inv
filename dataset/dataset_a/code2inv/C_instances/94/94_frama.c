/*@ ensures \result >= 0; */
int unknown1();
/*@ ensures \result >= 0; */
int unknown2();

void fmain() {
  // variable declarations
  int i;
  int j;
  int k = unknown1();
  int n = unknown2();
  // pre-conditions
  
  
  i = 0;
  j = 0;
  // loop body
  while (i <= n) {
    i  = i + 1;
    j  = j + i;
  }
  // post-condition
  //@ assert( ((i + (j + k)) > (2 * n)) );
}
