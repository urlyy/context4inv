int main() {
  int n,i,j;
  int unknown1, unknown2, unknown3;
  n = unknown1;
  if(n <= 500000){
    i = 0; j=0;
    while(i<n){ 
      if(unknown2!=0){
        i = i + 6; 
      }else{
        i = i + 3; 
      }
      unknown2 = unknown3; 
    }
    //@ assert((n <= 500000) => (i%3==0) );
  }
  
  return 0;
}
