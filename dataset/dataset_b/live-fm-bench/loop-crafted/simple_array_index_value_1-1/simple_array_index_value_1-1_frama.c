int foo(int *array)
{
  int SIZE=1000;
  unsigned int index;
  for (index = 0; index < SIZE; index++) {
    array[index] = (index % 2);
  }
  //@ assert( \forall int j; ((0 <= j && j < SIZE) ==> ((j % 2 == 0 ==> array[j] == 0) && (j % 2 != 0 ==> array[j] != 0))) );
  return 0;
}
