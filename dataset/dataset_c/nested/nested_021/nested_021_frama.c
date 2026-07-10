int main() {
  int N = 4;
  int M = 3;
  int i, j;
  int a = 0;
  int b = 0;

  for (i = 0; i < N; i++) {
    a = a + i;
    for (j = 0; j < M; j++) {
      b = b + j;
    }
  }

  //@ assert(a == 6 && b == 12);
  return 0;
}
