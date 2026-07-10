int main(int N, int *a)
{
	if(N > 0){
		//@ assume(N <= 2147483647/4);
		int i;
		int sum[1];
		for(i=0; i<N; i++)
		{
			a[i] = i%1;
		}
		for(i=0; i<N; i++)
		{
			if(i==0) {
				sum[0] = 0;
			} else {
				sum[0] = sum[0] + a[i];
			}
		}
		//@ assert(sum[0] == 0);
	}
	return 1;
}
