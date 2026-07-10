int foo(int SIZE, int *a)
{
	int MAX = 100000;
	if(SIZE > 1 && SIZE < MAX)
	{
		int i;
		for(i=0; i<SIZE; i++)
		{
			if( i >> 16 > 250)
			{
				a[i] = 1;
			}
			else
			{
				a[i] = 0;
			}
		}
		//@ assert(\forall int k; ((k >= 0 && k < SIZE) ==> (a[k] == 0)));
	}
	return 1;
}
