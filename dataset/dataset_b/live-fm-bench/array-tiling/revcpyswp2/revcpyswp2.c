int main(int SIZE, int *a, int *b, int *a_copy, int *b_copy)
{
	int MAX = 100000;
	if(SIZE > 1 && SIZE < MAX)
	{
		int i;
		int tmp;
		for(i=0; i<SIZE; i++)
		{
			a[i] = a_copy[SIZE-i-1];
			b[i] = b_copy[SIZE-i-1];
		}
		for(i=0; i<SIZE; i++)
		{
			tmp = a[i];
			a[i] = b[i];
			b[i] = tmp;
		}
		for(i=0; i<SIZE; i++)
		{
			tmp = a[i];
			a[i] = b[i];
			b[i] = tmp;
		}
		//@ assert(∀ k ((k >= 0 && k < SIZE) => (a[k] == a_copy[SIZE - k - 1])));
	}
	return 1;
}
