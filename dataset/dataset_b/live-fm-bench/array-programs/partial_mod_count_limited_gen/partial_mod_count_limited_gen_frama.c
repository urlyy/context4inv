/*@
  requires 0 < lim && lim < N/R;
  requires N == 1000;
  requires R > 1 && R < 6;
*/
int foo(int lim, int N, unsigned int R){
  int i,j=0,k=0,a[N];
  
  for(i=0;i<N;i++){
    a[i]=i+1;
    if(i>N/R && k<lim)
       a[i]=i%R;
    if(a[i]==0) k++;
  }
  for(i=0;i<N;i++){
    if (a[i]==0) j++;
  }
  //@ assert(j <= ((N*(R-1))/(R*R)));
  return 0;
}
