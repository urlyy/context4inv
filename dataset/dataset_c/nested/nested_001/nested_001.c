int main() {
  int N = 4;
  int M = 3;
  int i, j;
  int acc = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      acc = acc + i;
    }
  }

  //@ assert(acc == 18);
  return 0;
}
