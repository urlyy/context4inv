int main() {
  int N = 3;
  int M = 3;
  int i, j;
  int p = 1;
  int q = 0;

  for (i = 1; i <= N; i++) {
    for (j = 1; j <= M; j++) {
      p = p + i * j;
      q = q + 1;
    }
  }

  //@ assert(q == 9 && p == 37);
  return 0;
}
