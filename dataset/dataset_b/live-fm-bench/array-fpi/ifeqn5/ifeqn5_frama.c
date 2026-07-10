/*@
  requires N <= 2147483647/4;
*/
int foo(int N, int *a, int *b)
{
	if(N > 0){
		
		int i;
		for(i=0; i<N; i++)
		{
			if(i==0) {
				a[0] = 10;
			} else {
				a[i] = a[i-1] + 10;
			}
		}
		for(i=0; i<N; i++)
		{
			if(i==0) {
				b[0] = 1;
			} else {
				b[i] = b[i-1] + a[i-1];
			}
		}
		//@ assert( \forall int j; ((0 <= j && j < N) ==> (b[j] == 5*j*j + 5*j + 1)) );
	}
	return 1;
}
