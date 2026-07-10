int main(int *vectorx)
{
    int i;
    int n = 100000;
    int pos;
    int element;
    int found = 0;
    for (i = 0; i < n && found!=0; i++)
    {
        if (vectorx[i] == element)
        {
            found = 1;
            pos = i;
        }
    }
    if ( found !=0 )
    {
        for (i = pos; i <  n - 1; i++)
        {
            vectorx[i] = vectorx[i + 1];
        }
        //@ assert( (found!=0) => ∀x((0 <= x && x < pos) => (vectorx[x] != element)) );
    }
  return 0;
}
