int main( int *a,int *b) {
  int N = 100000;
  int marker;
  int pos;
  if ( pos >= 0 && pos < N ) {
    a[ pos ] = marker;
    int i = 0;
    while( a[ i ] != marker ) {
      i = i + 1;
    }
    //@ assert(i <= pos  );
  }
  return 0;
}
