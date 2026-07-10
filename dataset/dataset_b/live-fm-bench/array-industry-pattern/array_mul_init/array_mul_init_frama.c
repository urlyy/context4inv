int foo(int *a, int *b)
{
	int SIZE=100000;
	int k;
	int i;
	for (i  = 0; i<SIZE ; i++)
	{
		a[i] = i; 
		b[i] = i ;
	}
	for (i=0; i< SIZE; i++)
	{
		if(unknown())
		{
			k = unknown();
			a[i] = k;
			b[i] = k * k;
		}
	}
	//@ assert( \forall int j; ((0 <= j && j < SIZE) ==> (a[j] == b[j] || b[j] == a[j] * a[j])) );
	return 0;
}