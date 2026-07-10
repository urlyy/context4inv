int foo(int *array)
{
  int SIZE=1000;
  unsigned int index = 0;
  unsigned int tmp = 0;
  while (index < SIZE) {
    array[index] = tmp;
    index = index + 1;
    tmp = tmp + 2;
  }
  //@ assert( \forall int j; ((0 <= j && j < SIZE) ==> ((array[j] == 2*j) || (array[j] == 0))) );
  return 0;
}
