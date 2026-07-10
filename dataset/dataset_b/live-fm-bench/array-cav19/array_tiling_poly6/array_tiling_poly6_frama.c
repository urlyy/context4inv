/*@ ensures \result >1; */
int unknown1();

int foo(int *a)
{
  int S = unknown1();
  int i;
  for(i=0;i<S;i++){
    a[i]=((i-1)*(i+1));
  }
  for(i=0;i<S;i++){
    a[i]=a[i]-(i*i);
  }
  //@ assert(\forall int k; (0<=k && k<S) ==> (a[k]==-1));
  return 0;
}
