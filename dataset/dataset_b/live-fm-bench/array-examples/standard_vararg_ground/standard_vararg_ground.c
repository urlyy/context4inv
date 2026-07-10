
int main( int *aa){
  int N = 100000;
  int a = 0;
  while( aa[a] >= 0 ) {
    a++;
  }
  //@ assert( ∀x((0 <= x && x < a) => (aa[x] >= 0)) );
  return 0;
}
