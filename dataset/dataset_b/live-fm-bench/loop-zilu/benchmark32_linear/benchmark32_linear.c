int main(int x) {
  if ((x==1 || x==2)){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      if(x==1) x=2;
      else if (x==2) x=1;
    }
    //@ assert(x<=8);
  }
  return 0;
}
