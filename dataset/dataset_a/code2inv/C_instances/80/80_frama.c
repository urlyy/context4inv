/*@
  requires x >= y;
  requires x >= 0;
  requires y >= 0;
*/
void ffoo(int x,int y) {
  // variable declarations
  int i;
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
  //@ assert((i < y)==>(i < x));
}