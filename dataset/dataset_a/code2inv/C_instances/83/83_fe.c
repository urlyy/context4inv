int main() {
  int y;
  // variable declarations
  int x;
  // pre-conditions
  x = -5000;
  // loop body
  while (x < 0) {
    x  = x + y;
    y  = y + 1;
  }
  // post-condition
  assert(y > 0);
}