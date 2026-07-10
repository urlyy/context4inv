int main ( int *a) {
  int N=100000;
  int e ;
  int i = 0;
  int j;
  while( i < N && a[i] != e ) {
    i = i + 1;
  }
  //@ assert( ∀x((0 <= x && x < i) => (a[x] != e)) );
  return 0;
}
