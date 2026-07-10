int main(int SIZE, int *a)
{
	int MAX = 100000;
	if(SIZE > 1 && SIZE < MAX)
	{
		int i;
		for(i=0; i<SIZE; i++)
		{
			a[i] = i*i + 2;
		}
		for(i=0; i<SIZE; i++)
		{
			a[i] = a[i] - 2;
		}
		//@ assert(∀ k ((k >= 0 && k < SIZE) => (a[k] == k*k)));
	}
	return 1;
}
