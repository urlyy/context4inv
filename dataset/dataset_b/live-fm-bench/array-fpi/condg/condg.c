int main(int N, int *a)
{
	if(N > 0){
		//@ assume(N <= 2147483647/4);
		int i;
		int sum[1];
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
			if(sum[0] == N) {
				a[i] = a[i] - 1;
			} else {
				a[i] = a[i] + 1;
			}
		}
		//@ assert( ∀j((0 <= j && j < N) => (a[j] == 0)) );
	}
	return 1;
}
