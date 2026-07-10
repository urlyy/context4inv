int main(int n) {
  // variable declarations
  int x;
  // pre-conditions
  x = n;
  // loop body
  while (x > 1) {
    x  = x - 1;
  }
  // post-condition
  //@ assert((n >= 1)=> (x == 1))
}
