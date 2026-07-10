int main(int N, int *a, int *b)
{
	if(N > 0){
		//@ assume(N <= 2147483647/4);
		int i;
		a[0] = 8;
		b[0] = 1;
		for(i=1; i<N; i++)
		{
			a[i] = a[i-1] + 8;
		}
		for(i=1; i<N; i++)
		{
			b[i] = b[i-1] + a[i-1];
		}
		//@ assert( ∀j((0 <= j && j < N) => (b[j] == 4*j*j + 4*j + 1)) );
	}
	return 1;
}
