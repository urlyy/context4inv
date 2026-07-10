int main() {
  int N = 3;
  int M = 4;
  int i, j;
  int x = 0;
  int y = 0;

  for (i = 1; i <= N; i++) {
    for (j = 1; j <= M; j++) {
      x = x + i;
      y = y + j;
    }
  }

  //@ assert(x == 24 && y == 30);
  return 0;
}
