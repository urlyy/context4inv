int main() {
  int x;int y;int n;
  if ((x>=0 && x<=y && y<n)){
    while (x<n) {
      x++;
      if (x>y) y++;
    }
    assert(y==n);
  }
  return 0;
}
