int main(int x,int y) {
  // variable declarations
  int i;
  int j;
  // pre-conditions
  i = x;
  j = y;
  // loop body
  while (x != 0) {
    x  = x - 1;
    y  = y - 1;
  }
  // post-condition
  //@ assert( (i == j)=>(y == 0) )
}
