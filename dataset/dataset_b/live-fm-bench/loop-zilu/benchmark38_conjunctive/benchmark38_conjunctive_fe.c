int main() {
  int x;
  int y;
  if ((x == y && y == 0)){
    while (unknown()) {
      x+=4;y++;
    }
    assert(x == 4*y && x >= 0);
  }
  return 0;
}
