
int main() {
  int n;
  int SIZE = 50000001;
  int i,j,k;
  if (n <= SIZE){
    i = 0; j=0;
    while(i<n){ 
      i = i + 4;
      j = i +2;    
    }
    k =i;
    while( (j%2) == 0){
      j-=4;
      k -=4; 
    }
    assert( (k%2) == 0 );
  }
  return 0;
}
