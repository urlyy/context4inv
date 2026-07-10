/*@
  requires N <= 2147483647/4;
*/
int foo(int N, int *a, int *b)
{
	if(N > 0){
		
		int i;
		a[0] = 6;
		b[0] = 1;
		for(i=1; i<N; i++)
		{
			a[i] = a[i-1] + 6;
		}
		for(i=1; i<N; i++)
		{
			b[i] = b[i-1] + a[i-1];
		}
		//@ assert( \forall int j; ((0 <= j && j < N) ==> (b[j] == 3*j*j + 3*j + 1)) );
	}
	return 1;
}
