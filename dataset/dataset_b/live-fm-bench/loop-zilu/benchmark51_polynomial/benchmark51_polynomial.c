int main(int x) {
  if (((x>=0) && (x<=50))){
    int unknown1, unknown2;
    while (unknown1!=0) {
      unknown1 = unknown2;
      if (x>50) x++;
      if (x == 0) { 
        x ++;
      } else x--;
    }
    //@ assert((x>=0) && (x<=50));
  }
  return 0;
}
