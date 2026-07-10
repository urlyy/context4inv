int main() {
  int N = 3;
  int M = 4;
  int i, j;
  int sum = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      sum = sum + j;
    }
  }

  //@ assert(sum == 18);
  return 0;
}
