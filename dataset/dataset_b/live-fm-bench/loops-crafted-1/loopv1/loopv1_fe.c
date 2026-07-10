int main() {
  int n,i,j;
  n = unknown();
  if(n <= 500000){
    i = 0; j=0;
    while(i<n){ 
      if(unknown()){
        i = i + 6; 
      }else{
        i = i + 3; 
      }
    }
    if(n <= 500000){
      assert((i%3==0) );
    }
  }
  
  return 0;
}