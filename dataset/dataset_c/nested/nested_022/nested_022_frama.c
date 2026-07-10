int main() {
  int N = 3;
  int M = 4;
  int i, j;
  int x = 0;
  int y = 0;
  int z = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      x = x + 1;
      y = y + i;
      z = z + j;
    }
  }

  //@ assert(x == 12 && y == 24 && z == 18);
  return 0;
}
