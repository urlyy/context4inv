int main() {
  int N;
  int M;
  int i, j;
  int total = 0;

  //@ assume(N >= 1 && N <= 8);
  //@ assume(M >= 1 && M <= 8);

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      total = total + i + j;
    }
  }

  //@ assert(total >= 0 && total <= N * M * (N + M));
  return 0;
}
