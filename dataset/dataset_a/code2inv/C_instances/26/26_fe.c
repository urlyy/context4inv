int main() {
  int n;
  // variable declarations
  int x;
  // pre-conditions
  x = n;
  // loop body
  while (x > 1) {
    x  = x - 1;
  }
  // post-condition
  if((x!=1)){assert((n<=0));}
}
