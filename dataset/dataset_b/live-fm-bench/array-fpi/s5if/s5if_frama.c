/*@
  requires N <= 2147483647/4;
*/
int foo(int N, int *a)
{
	if(N > 0){
		
		int sum[1];
		int i;
		sum[0] = 0;
		for(i=0; i<N; i++)
		{
			a[i] = 5;
		}
		for(i=0; i<N; i++)
		{
			if(a[i] == 5) {
				sum[0] = sum[0] + a[i];
			} else {
				sum[0] = sum[0] * a[i];
			}
		}
		//@ assert(sum[0] == 5*N);
	}
	return 1;
}
