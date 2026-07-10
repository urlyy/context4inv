int main() {
  int x;
  int y;
  if (x==1 && y==1){
    while (unknown()) {
      x=x+y;
      y=x;
    }
    assert(y>=1);
  }
  return 0;
}