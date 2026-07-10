int main(int N, int *a)
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
			if(a[i] == 1) {
				a[i] = a[i] + 2;
			} else {
				a[i] = a[i] - 1;
			}
		}
		for(i=0; i<N; i++)
		{
			if(a[i] == 3) {
				sum[0] = sum[0] + a[i];
			} else {
				sum[0] = sum[0] * a[i];
			}
		}
		//@ assert(sum[0] == 3*N);
	}
	return 1;
}
