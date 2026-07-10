int main(int x,int y,int z) {
  if ((y>0 || x>0 || z>0)){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      if (x>0) {
        x++;
      }
      if (y>0) {
        y++;
      } else {
        z++;
      }
    }
    //@ assert(x>0 || y>0 || z>0);
  }
 
  return 0;
}
