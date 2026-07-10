int main() {
  unsigned int x = 0;
  unsigned int y = 0;
  while (x < 1025) {
    y = 0;
    while (y < 10) {
      y++;
    }
    x++;
  }
  //@ assert(x % 2 == 1);
}
