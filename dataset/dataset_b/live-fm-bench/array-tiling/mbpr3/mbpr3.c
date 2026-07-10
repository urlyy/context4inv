int main(int CELLCOUNT)
{
	if(CELLCOUNT > 1 && CELLCOUNT %3 == 0)
	{
		int MINVAL=2;
		int i;
		int volArray[CELLCOUNT];
		int CCCELVOL3 = 7;
		int CCCELVOL2 = 3;
		int CCCELVOL1 = 1;
		for(i = 1; i <= CELLCOUNT/3; i++)
		{
			if(CCCELVOL3 >= MINVAL)
			{
				volArray[i*3 - 3] = CCCELVOL3;
			}
			else
			{
				volArray[i*3 - 3] = 0;
			}
			volArray[i*3 - 2] = volArray[i*3 - 2];
			volArray[i*3 - 1] = volArray[i*3 - 1];
		}
		for(i = 1; i <= CELLCOUNT/3; i++)
		{
			if(CCCELVOL2 >= MINVAL)
			{
				volArray[i*3 - 2] = CCCELVOL2;
			}
			else
			{
				volArray[i*3 - 2] = 0;
			}
			volArray[i*3 - 3] = volArray[i*3 - 3];
			volArray[i*3 - 1] = volArray[i*3 - 1];
		}
		for(i = 1; i <= CELLCOUNT/3; i++)
		{
			if(CCCELVOL1 >= MINVAL)
			{
				volArray[i*3 - 1] = CCCELVOL1;
			}
			else
			{
				volArray[i*3 - 1] = 0;
			}
			volArray[i*3 - 2] = volArray[i*3 - 2];
			volArray[i*3 - 3] = volArray[i*3 - 3];
		}
		//@ assert(∀ k ((k >= 0 && k < CELLCOUNT) => (volArray[k] >= MINVAL || volArray[k] == 0)));
	}
	return 1;
}
