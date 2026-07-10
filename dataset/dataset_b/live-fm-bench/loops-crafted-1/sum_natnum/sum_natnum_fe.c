int main() {
  int SIZE = 40000; 
  int i;
  int sum;
  i = 0, sum =0; 
  while(i< SIZE){ 
      i = i + 1; 
      sum += i;
  }
  assert( sum == ((SIZE *(SIZE+1))/2));
  return 0;
}
