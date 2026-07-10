/*@
  requires 0 < lim && lim < N/R;
  requires N == 1000000;
  requires R == 5;
*/
int foo(int lim, int N, unsigned int R){
  int i,j=0,k=0,a[N];
  
  for(i=0;i<N;i++){
    a[i]=i+1;
    if(i>N/2 && k<lim)
       a[i]=i%R;
    if(a[i]==0) k++;
  }
  for(i=0;i<N;i++){
    if (a[i]==0) j++;
  }
  //@ assert(j < N/(2*R));
  return 0;
}
