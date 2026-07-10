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
			sum[0] = sum[0] + 1;
		}
		for(i=0; i<N; i++)
		{
			a[i] = sum[0];
		}
		//@ assert( \forall int j; ((0 <= j && j < N) ==> (a[j] == N)) );
	}
	return 1;
}
