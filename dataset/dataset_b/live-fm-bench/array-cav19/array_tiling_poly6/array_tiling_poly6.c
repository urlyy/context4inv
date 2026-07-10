int main()
{
  int S;
  //@ assume(S>1)
  int i;
  int a[S];
  for(i=0;i<S;i++){
    a[i]=((i-1)*(i+1));
  }
  for(i=0;i<S;i++){
    a[i]=a[i]-(i*i);
  }
  //@ assert(∀k((0<=k && k<S)=>(a[k]==-1)))
  return 0;
}
