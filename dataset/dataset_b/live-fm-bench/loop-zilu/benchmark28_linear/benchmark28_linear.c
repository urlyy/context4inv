int main(int i,int j) {
  if ((i * i < j * j)){
    while (i < j) {
      j = j - i;
      if (j < i) {
        j = j + i;
        i = j - i;
        j = j - i;
      }
    }
    //@ assert(j == i);
  }
  return 0;
}
