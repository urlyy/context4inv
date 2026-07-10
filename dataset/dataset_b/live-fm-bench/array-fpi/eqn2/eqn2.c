int main(int N, int *a, int *b)
{
	if(N > 0){
		//@ assume(N <= 2147483647/4);
		int i;
		a[0] = 4;
		b[0] = 1;
		for(i=1; i<N; i++)
		{
			a[i] = a[i-1] + 4;
		}
		for(i=1; i<N; i++)
		{
			b[i] = b[i-1] + a[i-1];
		}
		//@ assert( ∀j((0 <= j && j < N) => (b[j] == 2*j*j + 2*j + 1)) );
	}
	return 1;
}
