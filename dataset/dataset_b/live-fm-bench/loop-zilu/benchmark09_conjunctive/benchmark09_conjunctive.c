int main(int x,int y) {
  if (x == y && y >=0){
    while (x!=0 && x>=0 && y>=0) {
      x--;
      y--;
    }
    //@ assert(y==0);
  }
  
  return 0;
}