/*@
  requires N <= 2147483647/4;
*/
int foo(int N, int *a,int *b)
{
	if(N > 0){
		
		int i;
		b[0] = 1;
		a[0] = N+1;
		for(i=1; i<N; i++)
		{
			b[i] = b[i-1] + 2;
		}
		for(i=1; i<N; i++)
		{
			a[i] = a[i-1] + b[i-1] + 2;
		}
		//@ assert( \forall int j; ((0 <= j && j < N) ==> (a[j] == N + (j+1)*(j+1))) );
	}
	return 1;
}
