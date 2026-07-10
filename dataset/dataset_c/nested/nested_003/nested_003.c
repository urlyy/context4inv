int main() {
  int A = 3;
  int B = 2;
  int C = 2;
  int i, j, k;
  int total = 0;

  for (i = 0; i < A; i++) {
    for (j = 0; j < B; j++) {
      for (k = 0; k < C; k++) {
        total = total + i + j;
      }
    }
  }

  //@ assert(total == 18);
  return 0;
}
