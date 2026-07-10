int main(int *a){
  int N = 100;
  int i,j=0;
  unsigned int R=1;
  for(i=0;i<N;i++){
    a[i]=i+1;
    if(i>N/2)
       a[i]=i % R;
  }
  for(i=0;i<N;i++){
    if (a[i]==0) j++;
  }
  //@ assert(j < N/2);
  return 0;
} 
