int main ( int *a) {
  int N=100000;
  int i = 0;
  while ( i < N ) {
    a[i] = 42;
    i = i + 1;
  }
  i = 0;
  while ( i < N ) {
    a[i] = 43;
    i = i + 1;
  }
  //@ assert( ∀x((0 <= x && x < N) => (a[x] == 43)) );
  return 0;
}
