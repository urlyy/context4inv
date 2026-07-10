int foo(int *a,int *b)
{
  int size = 10000;
  int i = 0;
  int j = 0;
  i = 1;
  while( i < size )
  {
	    a[j] = b[i];
        i = i+3;
        j = j+1;
  }
  //@ assert(\forall int j; ((0 <= j && 3*j < size) ==> (a[j] == b[3*j + 1])));
  return 0;
}
