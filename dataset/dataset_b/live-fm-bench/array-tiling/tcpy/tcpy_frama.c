/*@
  requires SIZE % 2 == 0;
*/
int foo(int SIZE, int *a, int *acopy)
{
	int MAX = 100000;
	if(SIZE > 1 && SIZE < MAX)
	{
		int i;
		for(i=0; i<SIZE/2; i++)
		{
			acopy[SIZE-i-1] = a[SIZE-i-1];
			acopy[i] = a[i];
		}
		//@ assert(\forall int k; ((k >= 0 && k < SIZE) ==> (acopy[k] == a[k])));
	}
	return 1;
}
