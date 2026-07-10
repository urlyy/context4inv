int foo(int *a,int *b)
{
  int size = 10000;
  int i = 0;
  int j = 0;
  while( i < size )
  {
	    a[j] = b[i];
      i = i+1;
      j = j+1;
  }
  //@ assert(\forall int k; ((0 <= k && k < size) ==> (a[k] == b[k])));
  return 0;
}
