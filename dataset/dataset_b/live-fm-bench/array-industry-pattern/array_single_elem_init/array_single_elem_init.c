int main(int *a,int *b,int *c)
{
	int SIZE=100000;
	int i;
	int q;
	int unknown1;
	for (i = 0; i < SIZE; i++)
	{
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
		q = unknown1;
	}
	//@ assert( ∀j((0 <= j && j < SIZE) => (j == 15000 => c[j] == 0)) );
	return 0;
}
