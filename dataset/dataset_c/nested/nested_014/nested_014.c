int main() {
  int N = 4;
  int i, j;
  int s = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < N; j++) {
      s = s + i + j;
    }
  }

  //@ assert(s == 48);
  return 0;
}
