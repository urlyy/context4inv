int foo(int *a,int *b)
{
  int size = 100000;
  int i = 0;
  int j = 0;
  i = 1;
  while( i < size )
  {
	a[j] = b[i];
        i = i+4;
        j = j+1;
  }
  //@ assert(\forall int j; ((0 <= j && j < size/4) ==> (a[j] == b[4*j+1])));
  i = 1;
  j = 0;
  return 0;
}
