int main() {
	int x = 0;
	int y = 0;

	int unknown1, unknown2;

	while(unknown1!=0) {
		y = y + 1;
		x = y * y;
		unknown1 = unknown2;
	}
	//@ assert(x == y * y)
	return 0;
}
