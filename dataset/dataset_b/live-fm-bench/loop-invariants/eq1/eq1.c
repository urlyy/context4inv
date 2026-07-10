int main(int w, int y) {
  int x = w;
  int z = y;
  int unknown1, unknown2, unknown3, unknown4;
  while (unknown1!=0) {
    unknown1 = unknown2;
    if (unknown3!=0) {
      ++w; ++x;
    } else {
      --y; --z;
    }
    unknown3=unknown4;
  }
  //@ assert(w == x && y == z);
  return 0;
}
