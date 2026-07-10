int main(int N, int *a, int *b)
{
	if(N > 0){
		//@ assume(N <= 2147483647/4);
		int i;
		for(i=0; i<N; i++)
		{
			if(i==0) {
				b[0] = 1;
			} else {
				b[i] = b[i-1] + 2;
			}
		}
		for(i=0; i<N; i++)
		{
			if(i==0) {
				a[0] = 1;
			} else {
				a[i] = a[i-1] + b[i-1] + 2;
			}
		}
		//@ assert( ∀j((0 <= j && j < N) => (a[j] == (j+1)*(j+1))) );
	}
	return 1;
}
