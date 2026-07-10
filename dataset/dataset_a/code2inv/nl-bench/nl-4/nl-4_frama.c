/*@ ensures \result >= 0; */
int unknown1();

/*@ ensures \result >= 0; */
int unknown2();

int main() {
	int x = unknown1();
	int y = unknown2();

	int z = x * y;

	while(x > 0) {
		x = x - 1;
		z = z - y;
	}
	//@ assert(z == 0);
	return 0;
}