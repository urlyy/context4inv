int main() {
  int N;
  int M;
  int i, j;
  int r = 0;

  //@ assume(N >= 0 && N <= 12);
  //@ assume(M >= 0 && M <= 12);

  for (i = 0; i < N; i++) {
    for (j = i; j < i + M; j++) {
      r = r + 1;
    }
  }

  //@ assert(r == N * M);
  return 0;
}
