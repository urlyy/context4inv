int main() {
  int N = 3;
  int M = 3;
  int K = 3;
  int i, j, k;
  int s = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      for (k = 0; k < K; k++) {
        s = s + k;
      }
    }
  }

  //@ assert(s == 27);
  return 0;
}
