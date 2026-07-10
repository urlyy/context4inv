int func(int x,int y) {
  // variable declarations
  int i;
  int j;
  int z1;
  int z2;
  int z3;
  // pre-conditions
  i = x;
  j = y;
  // loop body
  while (x != 0) {
    x  = x - 1;
    y  = y - 1;
  }
  // post-condition
  //@ assert( (y != 0)==>(i != j) );
  return 0;
}
