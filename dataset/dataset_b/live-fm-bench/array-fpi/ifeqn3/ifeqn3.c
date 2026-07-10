int main(int N, int *a, int *b)
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
		//@ assert( ∀j((0 <= j && j < N) => (b[j] == 3*j*j + 3*j + 1)) );
	}
	return 1;
}
