int main() {
  int N = 3;
  int M = 5;
  int i, j;
  int even = 0;
  int total = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      total = total + 1;
      if (j % 2 == 0) {
        even = even + 1;
      }
    }
  }

  //@ assert(total == 15 && even == 9);
  return 0;
}
