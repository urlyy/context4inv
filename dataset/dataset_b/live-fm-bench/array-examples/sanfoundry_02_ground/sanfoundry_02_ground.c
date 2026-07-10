int main(int *array)
{
    int MAX=100000;
    int i;
    int largest1;
    int largest2;
    int temp;
    largest1 = array[0];
    largest2 = array[1];
    if (largest1 < largest2)
    {
        temp = largest1;
        largest1 = largest2;
        largest2 = temp;
    }
    for (i = 2; i < MAX;  i++)
    {
        if (array[i] >= largest1)
        {
            largest2 = largest1;
            largest1 = array[i];
        }
        else if (array[i] > largest2)
        {
            largest2 = array[i];
        }
    }
    //@ assert(∀x((0 <= x && x < MAX) => (array[x] <= largest1 && (array[x] <= largest2 || array[x] == largest1))))
  return 0;
}
