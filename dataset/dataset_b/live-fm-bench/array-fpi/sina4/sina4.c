int main(int N, int *a, int *b)
{
	if(N > 0){
		//@ assume(N <= 2147483647/4);
		int sum[1];
		int i;
		sum[0] = 0;
		for(i=0; i<N; i++)
		{
			a[i] = 1;
		}
		for(i=0; i<N; i++)
		{
			sum[0] = sum[0] + a[i];
		}
		for(i=0; i<N; i++)
		{
			a[i] = a[i] + sum[0];
		}
		for(i=0; i<N; i++)
		{
			b[i] = a[i] + 1;
		}
		//@ assert( ∀j((0 <= j && j < N) => (a[j] == N + 1)) );
	}
	return 1;
}
