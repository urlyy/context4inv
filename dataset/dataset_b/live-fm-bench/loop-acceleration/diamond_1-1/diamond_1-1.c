int main(int y) {
  int x = 0;
  while (x < 99) {
    if (y % 2 == 0) {
      x += 2;
    } else {
      x++;
    }
  }
  //@ assert((x % 2) == (y % 2));
}
