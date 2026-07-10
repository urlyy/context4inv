int main() {
  int N = 3;
  int M = 4;
  int i, j;
  int s = 0;
  int t = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      s = s + 1;
    }
    t = t + i;
  }

  //@ assert(s == 12 && t == 3);
  return 0;
}
