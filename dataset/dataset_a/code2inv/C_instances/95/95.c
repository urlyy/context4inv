int main() {
  // variable declarations
  int i;
  int j;
  int x;
  int y;
  // pre-conditions
  j = 0;
  i = 0;
  y = 1;
  // loop body
  while (i <= x) {
    i  = i + 1;
    j  = j + y;
  }
  // post-condition
  //@ assert((y == 1)=>(i == j))
}
