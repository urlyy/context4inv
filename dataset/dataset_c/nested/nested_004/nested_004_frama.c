int main() {
  int N = 5;
  int M = 2;
  int i, j;
  int x = 0;
  int y = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      x = x + 1;
      y = y + i;
    }
  }

  //@ assert(x == 10 && y == 20);
  return 0;
}
