int main(int* a1,int* a2,int* a3) {
  int N=200000;
  int i; 
  int z;
  z = 150000;
  for ( i = 0 ; i < N ; i++ ) {
      if (i != z){
        a2[i] = a1[i];
      }
  }
  for ( i = 0 ; i < N ; i++ ) {
      if (i != z){
         a3[i] = a2[i];
      }
      else{
          a3[i] = a1[i];
      }
  }
  //@ assert(∀ k ((k >= 0 && k < N) => (a1[k] == a3[k])));
  return 0;
}
