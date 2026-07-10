int foo(int w, int y) {
  int x = w;
  int z = y;
  while (unknown()) {
    if (unknown()) {
      ++w; ++x;
    } else {
      --y; --z;
    }
  }
  //@ assert(w == x && y == z);
  return 0;
}