int main() {
  int N = 4;
  int M = 2;
  int i, j;
  int x = 1;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      x = x + 2;
    }
  }

  //@ assert(x == 17);
  return 0;
}
