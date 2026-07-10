int main() {
  int n;
  // variable declarations
  int x;
  // pre-conditions
  x = 0;
  // loop body
  while (x < n) {
    x  = x + 1;
  }
  // post-condition
  if((n >= 0)){assert((x == n));}
}
