int main(int i,int j,int x,int y,int k) {
  j=0;
  if ((x+y==k)){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      if(j==i) {x++;y--;} else {y++;x--;} j++;
    }
    //@ assert(x+y==k);
  }
  return 0;
}
