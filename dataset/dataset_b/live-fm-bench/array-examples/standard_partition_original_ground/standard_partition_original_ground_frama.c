int foo( int *aa,int *bb,int *cc) {
  int N = 100000;
  int a = 0;
  int b = 0;
  int c = 0;
  while( a < N ) {
    if( aa[ a ] >= 0 ) {
      bb[ b ] = aa[ a ];
      b = b + 1;
    }
    else {
      cc[ c ] = aa[ a ];
      c = c + 1;
    }
    a = a + 1;
  }
  //@ assert( (\forall int x;((0 <= x && x < b) ==> (bb[x] >= 0))) && (\forall int x;((0 <= x && x < c) ==> (cc[x] < 0))) );
  return 0;
}
