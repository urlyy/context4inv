int main(int x) {
  int y = x;
  while (x < 1024) {
    x++;
    y++;
  }
  //@ assert(x == y);
}
