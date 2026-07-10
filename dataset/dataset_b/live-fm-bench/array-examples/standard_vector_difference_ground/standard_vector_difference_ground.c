int main(int *a,int *b,int *c ) {
  int SIZE = 100000;
  int i = 0;
	i = 0;
  while (i < SIZE) {
    c[i] = a[i] - b[i];
    i = i + 1;
  }
  //@ assert( ∀x((0 <= x && x < SIZE) => (c[x] == a[x] - b[x])) );
  return 0;
}
