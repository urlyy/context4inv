int main(int SIZE, int *a)
{
	int MAX = 100000;
	if(SIZE > 1 && SIZE < MAX)
	{
		int i;
		for( i = 0; i < SIZE ; i++ )
		{
			if((i+1) < SIZE )
			{
				a[i+1] = i;
			}
			a[i] = i;
		}
		//@ assert(∀ k ((k >= 0 && k < SIZE) => (a[k] >= k)));
	}
	return 1;
}
