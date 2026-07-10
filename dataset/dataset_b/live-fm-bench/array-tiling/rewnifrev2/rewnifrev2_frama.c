int foo(int SIZE, int *a)
{
	int MAX = 100000;
	int i;
	if(SIZE > 1 && SIZE < MAX)
	{
		for( i=SIZE-2; i >= 0; i-- )
		{
			a[i] = i;
			a[i+1] = i+1;
		}
		//@ assert(\forall int k; ((k >= 0 && k < SIZE) ==> (a[k] >= k)));
	}
	return 1;
}
