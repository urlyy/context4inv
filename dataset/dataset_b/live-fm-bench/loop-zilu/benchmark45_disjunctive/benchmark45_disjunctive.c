int main(int x,int y) {
  if ((y>0 || x>0)){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      if (x>0) {
        x++;
      } else {
        y++;
      }
    }
    //@ assert(x>0 || y>0);
  }
  return 0;
}
