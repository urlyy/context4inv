int foo(int SIZE, int *a)
{
	int MAX = 100000;
	if(SIZE > 1 && SIZE < MAX)
	{
		int i;
		int val2 = 3;
		int val1 = 0;
		int low=2;
		for(i = 0; i < SIZE; i++)
		{
			if(i+1 < SIZE)
			{
				a[i+1] = val1;
			}
			a[i] = val2;
		}
		//@ assert(\forall int k; ((k >= 0 && k < SIZE) ==> (a[k] >= low)));
	}
	return 1;
}
