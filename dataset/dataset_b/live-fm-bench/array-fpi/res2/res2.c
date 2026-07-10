int main(int N, int *a,int *b,int *c)
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
			b[i] = 1;
		}
		for(i=0; i<N; i++)
		{
			sum[0] = sum[0] + b[i];
		}
		for(i=0; i<N; i++)
		{
			c[i] = 1;
		}
		for(i=0; i<N; i++)
		{
			sum[0] = sum[0] + c[i];
		}
		//@ assert(sum[0] <= 3*N);
	}
	return 1;
}
