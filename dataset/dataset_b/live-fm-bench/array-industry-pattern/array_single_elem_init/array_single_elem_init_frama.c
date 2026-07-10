int foo(int *a,int *b,int *c)
{
	int SIZE=100000;
	int i;
	int q;
	for (i = 0; i < SIZE; i++)
	{
		q = unknown();
		a[i] = 0;
		if (q == 0)
		{
			a[i] = 1;
			b[i] = i % 2;
		}
		if (a[i] != 0)
		{
			if (b[i] == 0)
			{
				c[i] = 0;
			}
			else
			{
				c[i] = 1;
			}
		}
	}
	//@ assert( \forall int j; ((0 <= j && j < SIZE) ==> (j == 15000 ==> c[j] == 0)) );
	return 0;
}