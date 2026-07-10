int main() {
  int N = 4;
  int M = 3;
  int i, j;
  int acc = 0;
  int steps = 0;

  for (i = 1; i <= N; i++) {
    for (j = 1; j <= M; j++) {
      acc = acc + i * j;
      steps = steps + 1;
    }
  }

  //@ assert(steps == 12 && acc == 120);
  return 0;
}
