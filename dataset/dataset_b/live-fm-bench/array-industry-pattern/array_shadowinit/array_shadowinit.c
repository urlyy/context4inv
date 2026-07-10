int main(int N,int *a) {
 if(N>0) {
  int i,k;
  i=0;
  k=0;
  while(i < N) {
   a[k]=k;
   i=i+1;
   k=k+1;
  }
  //@ assert( ∀j((0 <= j && j < N) => (a[j] == j)) );
 }
 return 0;
}
