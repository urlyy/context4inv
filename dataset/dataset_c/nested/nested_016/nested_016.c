int main() {
  int N = 4;
  int M = 3;
  int i, j;
  int r = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      r = r + i * 2 + j;
    }
  }

  //@ assert(r == 45);
  return 0;
}
