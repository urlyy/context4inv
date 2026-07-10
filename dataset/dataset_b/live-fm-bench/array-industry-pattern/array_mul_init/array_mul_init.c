int main(int *a, int *b)
{
	int SIZE=100000;
	int k;
	int i;
	for (i  = 0; i<SIZE ; i++)
	{
		a[i] = i; 
		b[i] = i ;
	}
	int unknown1, unknown2, unknown3;
	for (i=0; i< SIZE; i++)
	{
		if(unknown1!=0)
		{
			unknown1 = unknown2;
			a[i] = k;
			b[i] = k * k;
			k = unknown3;
		}
	}
	//@ assert( ∀j((0 <= j && j < SIZE) => (a[j] == b[j] || b[j] == a[j] * a[j])) );
}
