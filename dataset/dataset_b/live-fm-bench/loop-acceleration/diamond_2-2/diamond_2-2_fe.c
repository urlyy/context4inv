int main() {
  int y;
  int x = 0;
  while (x < 99) {
    if (y % 2 == 0) x += 2;
    else x++;
    if (y % 2 == 0) x += 2;
    else x -= 2;
    if (y % 2 == 0) x += 2;
    else x += 2;
    if (y % 2 == 0) x += 2;
    else x -= 2;
    if (y % 2 == 0) x += 2;
    else x += 2;
    if (y % 2 == 0) x += 2;
    else x -= 4;
    if (y % 2 == 0) x += 2;
    else x += 4;
    if (y % 2 == 0) x += 2;
    else x += 2;
    if (y % 2 == 0) x += 2;
    else x -= 4;
    if (y % 2 == 0) x += 2;
    else x -= 4;
  }
  assert((x % 2) == (y % 2));
  return 0;
}
