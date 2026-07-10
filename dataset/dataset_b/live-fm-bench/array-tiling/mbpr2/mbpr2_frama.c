int foo(int CELLCOUNT)
{
	if(CELLCOUNT > 1 && CELLCOUNT % 2 == 0)
	{
		int MINVAL=2;
		int i;
		int volArray[CELLCOUNT];
		int CCCELVOL2 = 3;
		int CCCELVOL1 = 1;
		for(i = 1; i <= CELLCOUNT/2; i++)
		{
			if(CCCELVOL2 >= MINVAL)
			{
				volArray[i*2 - 2] = CCCELVOL2;
			}
			else
			{
				volArray[i*2 - 2] = 0;
			}
			volArray[i*2 - 1] = volArray[i*2 - 1];
		}
		for(i = 1; i <= CELLCOUNT/2; i++)
		{
			if(CCCELVOL1 >= MINVAL)
			{
				volArray[i*2 - 1] = CCCELVOL1;
			}
			else
			{
				volArray[i*2 - 1] = 0;
			}
			volArray[i*2 - 2] = volArray[i*2 - 2];
		}
		//@ assert(\forall int k; ((k >= 0 && k < CELLCOUNT) ==> (volArray[k] >= MINVAL || volArray[k] == 0)));
	}
	return 1;
}
