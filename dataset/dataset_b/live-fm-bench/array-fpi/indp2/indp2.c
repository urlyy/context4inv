int main(int N, int *a)
{
	if(N > 0){
		//@ assume(N <= 2147483647/4);
		int i;
		for(i=0;i<N;i++)
		{
			a[i]=((i-1)*(i+1));
		}
		for(i=0;i<N;i++)
		{
			a[i]=a[i]-(i*i);
		}
		for(i=0;i<N;i++)
		{
			a[i]=a[i]+1;
		}
		//@ assert( ∀j((0 <= j && j < N) => (a[j] == 0)) );
	}
	return 1;
}
