int main(int *a, int *b, int *c) {
  int SIZE = 100000;
  int i = 0;
  int rv = 1;
  while ( i < SIZE ) {
    if ( a[i] != b[i] ) {
      rv = 0;
    }
    c[i] = a[i];
    i = i+1;
  }
  //@ assert( ∀x((0 <= x && x < SIZE) => ((rv != 0 => (a[x] == b[x])) && (a[x] == c[x]))) );
  return 0;
}
