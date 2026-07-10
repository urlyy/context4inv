int main( int *a) {
  int N = 100000;
  int min = 0;
  int i = 0;
  while ( i < N ) {
    if ( a[i] < min ) {
      min = a[i];
    }
    i = i + 1;
  }
  //@ assert( ∀x((0 <= x && x < N) => (a[x] >= min)) );
  return 0;
}
