/*@
  requires N <= 2147483647/4;
*/
int foo(int N, int *a)
{
	if(N > 0){
		
		int i;
		for(i=0; i<N; i++)
		{
			if(a[i] < N) {
				a[i] = a[i];
			} else {
				a[i] = N;
			}
		}
		//@ assert( \forall int j; ((0 <= j && j < N) ==> (a[j] <= N)) );
	}
	return 1;
}
