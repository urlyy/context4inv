
int main() {
  int i;
  int c;
  if (c==0 && i==0){
    while (i<100 && i>0) {
      c=c+i;
      i=i+1;
    }
    assert(c>=0);
  }
  return 0;
}
