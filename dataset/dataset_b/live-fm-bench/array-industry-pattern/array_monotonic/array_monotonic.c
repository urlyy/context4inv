int main(int *a, int *b)
{
	int SIZE=100000;
	int i;
	for(i = 0; i < SIZE;  i = i + 2)
	{
		if(a[i] == 10){
			b[i] = 20;
		}
	}
	//@ assert( ∀j((0 <= j && j < SIZE && j % 2 == 0) => (a[j] == 10 => b[j] == 20)) );
}
