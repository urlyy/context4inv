int main(int n) {
  // variable declarations
  int v1;
  int v2;
  int v3;
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
