int foo(int *a)
{
	int SIZE = 10000000;
	int i;
	for(i=0;i<SIZE;i++)
	{
		a[i] = 0 ;
	}
	for(i=0;i<SIZE/2;i++)
	{
		a[i] = 10 ;
	}
	//@ assert( \forall int j; ((0 <= j && j < SIZE/2) ==> (a[j] == 10)) );
	return 0;
}	
