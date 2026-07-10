int main (int *a, int *b ) {
  int N=100000;
  int i = 0;
  while ( i < N ) {
    a[i] = 42;
    i = i + 1;
  }
  for ( i = 0 ; i < N ; i++ ) {
    b[i] = a[i];
  }
  for ( i = 0 ; i < N ; i++ ) {
    b[i] = b[i] + i;
  }
  for ( i = 0 ; i < N ; i++ ) {
    b[i] = b[i] - a[i];
  }
  //@ assert( ∀x((0 <= x && x < N) => (b[x] == x)) );
  return 0;
}
