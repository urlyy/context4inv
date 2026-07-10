int foo(int* password, int* guess) {
  int SIZE=100000;
  int i;
  int result = 1;
  for ( i = 0 ; i < SIZE ; i++ ) {
    if ( password[ i ] != guess[ i ] ) {
      result = 0;
    }
  }
  //@ assert( result != 0 ==> \forall int x;((0 <= x && x < SIZE) ==> (password[x] == guess[x])) );
  return 0;
}
