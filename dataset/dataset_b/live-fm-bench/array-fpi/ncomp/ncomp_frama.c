/*@
  requires N <= 2147483647/4;
*/
int foo(int N, int *a,int *b,int *c)
{
	if(N > 0){
		
		int i;
		a[0] = 6;
		b[0] = 1;
		c[0] = N;
		for(i=1; i<N; i++)
		{
			a[i] = a[i-1] + 6;
		}
		for(i=1; i<N; i++)
		{
			b[i] = b[i-1] + a[i-1];
		}
		for(i=1; i<N; i++)
		{
			c[i] = c[i-1] + b[i-1];
		}
		//@ assert( \forall int j; ((0 <= j && j < N) ==> (c[j] == N + j*j*j)) );
	}
	return 1;
}
