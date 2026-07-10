int main(int *array)
{
    int SIZE=100000;
    int i;
    int largest = array[0];
    for (i = 1; i < SIZE; i++)
    {
        if (largest < array[i]){
            largest = array[i];
        }
    }
    //@ assert( ∀x((0 <= x && x < SIZE) => (largest >= array[x])) );
    return 0;
}
