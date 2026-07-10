int foo()
{
  unsigned int i = 0;
  unsigned int j = 0;
  unsigned int k = 0;
  while (k < 1025) {
    i = i + 1;
    j = j + 2;
    k = k + 3;
  }
  //@ assert((k == 3*i) && (j == 2*i));
  return 0;
}
