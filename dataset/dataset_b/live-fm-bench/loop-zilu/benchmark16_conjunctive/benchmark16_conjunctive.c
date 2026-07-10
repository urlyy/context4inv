int main(int i,int k) {
  if (0 <= k && k <= 1 && i == 1){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      i = i + 1;
      k = k - 1;
    }
    //@ assert(1 <= i + k && i + k <= 2 && i >= 1);
  }
  
  return 0;
}
