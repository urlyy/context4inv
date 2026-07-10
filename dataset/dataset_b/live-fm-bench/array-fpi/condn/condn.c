int main(int N, int *a)
{
	if(N > 0){
		//@ assume(N <= 2147483647/4);
		int i;
		for(i=0; i<N; i++)
		{
			if(a[i] < N) {
				a[i] = a[i];
			} else {
				a[i] = N;
			}
		}
		//@ assert( ∀j((0 <= j && j < N) => (a[j] <= N)) );
	}
	return 1;
}
