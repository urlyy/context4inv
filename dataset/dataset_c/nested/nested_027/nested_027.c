int main() {
  int N;
  int M;
  int i, j;
  int sum = 0;

  //@ assume(N >= 1 && N <= 8);
  //@ assume(M >= 1 && M <= 8);

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      sum = sum + 1;
    }
  }

  //@ assert(sum == N * M);
  return 0;
}
