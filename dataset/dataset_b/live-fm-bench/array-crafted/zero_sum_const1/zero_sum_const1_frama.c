/*@
  requires 1 < SIZE && SIZE < 100000;
*/
int foo(int *a, int SIZE)
{
	int MAX = 100000;
	
	int i, sum=0;
	if(SIZE > 1 && SIZE < MAX){
		for(i = 0; i < SIZE; i++ )
		{
			a[i] = 1;
		}
		for(i = 0; i < SIZE; i++ )
		{
			sum = sum + a[i];
		}
		for(i = 0; i < SIZE; i++)
		{
			sum = sum - a[i];
		}
		//@ assert(sum == 0);
	}
	return 1;
}
