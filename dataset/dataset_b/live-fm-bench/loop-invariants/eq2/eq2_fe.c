int main() {
  int w;
  int x = w;
  int y = w + 1;
  int z = x + 1;
  while (unknown()) {
    y++;
    z++;
  }
  assert(y == z);
  return 0;
}