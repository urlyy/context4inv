int main(int N, int *a, int *b, int *c)
{
	if(N > 0){
		//@ assume(N <= 2147483647/4);
		int i;
		for(i=0; i<N; i++)
		{
			if(i==0) {
				a[0] = 6;
			} else {
				a[i] = a[i-1] + 6;
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
		for(i=0; i<N; i++)
		{
			if(i==0) {
				c[0] = N;
			} else {
				c[i] = c[i-1] + b[i-1];
			}
		}
		//@ assert( ∀j((0 <= j && j < N) => (c[j] == N + j*j*j)) );
	}
	return 1;
}
