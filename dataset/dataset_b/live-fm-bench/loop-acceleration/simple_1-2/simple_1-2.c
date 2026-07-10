int main() {
  unsigned int x = 0;
  while (x < 1025) {
    x += 2;
  }
  //@ assert((x % 2)==0);
  return 0;
}
