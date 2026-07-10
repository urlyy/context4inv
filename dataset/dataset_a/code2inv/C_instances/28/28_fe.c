int main() {
  int n;
  // variable declarations
  int x;
  // pre-conditions
  x = n;
  // loop body
  while (x > 0) {
    x  = x - 1;
  }
  // post-condition
  if((x != 0)){assert((n < 0));}
}
