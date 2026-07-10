/*@ ensures \result >= 0 && \result >= y; */
int unknown1();
/*@ ensures \result >= 0; */
int unknown2();

void fmain() {
  // variable declarations
  int i;
  int x = unknown1();
  int y = unknown2();
  int z1;
  int z2;
  int z3;
  // pre-conditions
  i = 0;
  
  
  
  // loop body
  while (unknown()) {
    if (i < y){
      i  = i + 1;
    }
  }
  // post-condition
  //@ assert((i >= x && 0 > i)==>(i >= y));
}