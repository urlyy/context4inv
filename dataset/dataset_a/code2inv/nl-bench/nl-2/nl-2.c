int main() {
	int x;
	//@ assume(x >= 0)
	int y = x * x;
	int unknown1,unknown2;
	while(unknown1!=0) {
		x = x + 1;
		y = y + 1;
		unknown1 = unknown2;
	}
	//@ assert(y <= x * x)
	return 0;
}


