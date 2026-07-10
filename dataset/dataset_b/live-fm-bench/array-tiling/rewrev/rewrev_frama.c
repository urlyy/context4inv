int foo(int SIZE, int *a)
{
	int MAX = 100000;
	if(SIZE > 1 && SIZE < MAX)
	{
		int i;
		int val2 = 3;
		int val1 = 7;
		int low=2;
		for(i=SIZE-2; i >= -1; i--)
		{
			if(i >= 0)
			{
				a[i] = val1;
			}
			a[i+1] = val2;
		}
		//@ assert(\forall int k; ((k >= 0 && k < SIZE) ==> (a[k] >= low)));
	}
	return 1;
}
