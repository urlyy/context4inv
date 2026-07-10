int main() {
  int N = 3;
  int M = 3;
  int i, j;
  int a = 0;
  int b = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      a = a + i + j;
      b = b + i * j;
    }
  }

  //@ assert(a == 18 && b == 9);
  return 0;
}
