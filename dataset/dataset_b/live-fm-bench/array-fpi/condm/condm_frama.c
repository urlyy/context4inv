/*@
  requires N <= 2147483647/4;
*/
int foo(int N, int *a)
{
	if(N > 0){
		
		int i;
		for (i = 0; i < N; i++)
		{
			a[i] = 0;
		}
		for (i = 0; i < N; i++)
		{
			if (N%2 == 0) {
				a[i] = a[i] + 2;
			} else {
				a[i] = a[i] + 1;
			}
		}
		//@ assert( \forall int j; ((0 <= j && j < N) ==> (a[j] % 2 == N % 2)) );
	}
	return 1;
}
