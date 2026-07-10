/*@ ensures \result > 0 && \result < 10000; */
int unknown1();

/*@
  requires n < 100000;
  requires j>0 && j < 10000;
*/
int foo(int *a, int j, int n)
{
  int i;
  for(i=1;i<n;i++) {
    int unknown_1 = unknown1();
    a[i]=i+j+unknown_1;
  }
  //@ assert(\forall int k; (1 <= k && k < n) ==> (a[k] >= (k + 2)));
  return 0;
}