/*@ ensures \result >1 && \result < 1073741823; */
int unknown1();

int foo(int *a, int *acopy)
{
  int S = unknown1();
  int i;
  for(i=0;i < S;i++) {
    acopy[2*S - (i+1)] = a[2*S - (i+1)];
    acopy[i] = a[i];
  }
  //@ assert(\forall int k; (0<=k && k<2*S) ==> (acopy[k] == a[k]));
  return 0;
}
