int main(int SIZE, int *a)
{
	int MAX = 100000;
	if(SIZE > 1 && SIZE < MAX)
	{
		int i;
		for( i=SIZE-1; i>=0; i-- )
		{
			if((i-1) >= 0 )
			{
				a[i-1] = i-2;
			}
			a[i] = i;
		}
		//@ assert(∀ k ((k >= 0 && k < SIZE) => (a[k] >= k)));
	}
	return 1;
}
