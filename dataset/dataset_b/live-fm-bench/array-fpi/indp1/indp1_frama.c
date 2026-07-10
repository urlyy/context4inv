/*@
  requires N <= 2147483647/4;
*/
int foo(int N, int *a)
{
	if(N > 0){
		
		int i;
		for(i=0;i<N;i++)
		{
			a[i]=((i+1)*(i+1));
		}
		for(i=0;i<N;i++)
		{
			a[i]=a[i]-(i*i);
		}
		for(i=0;i<N;i++)
		{
			a[i]=a[i]-i;
		}
		//@ assert( \forall int j; ((0 <= j && j < N) ==> (a[j] == j + 1)) );

	}
	return 1;
}
