int main(int N, int *a)
{
	if(N > 0){
		//@ assume(N <= 2147483647/4);
		int i;
		int sum[1];
		for(i=0; i<N; i++)
		{
			if(i%1==0) {
				a[i] = 1;
			} else {
				a[i] = 0;
			}
		}
		for(i=0; i<N; i++)
		{
			if(i==0) {
				sum[0] = 0;
			} else {
				sum[0] = sum[0] + a[i];
			}
		}
		//@ assert(sum[0] <= N);
		return 1;
	}
}
