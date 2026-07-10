/*@ ensures \result >= 0; */
int unknown1();

/*@ ensures \result >= \result; */
int unknown2();

int main() {
	int x = unknown1();
	int y = unknown2();
	int z, w;

	z = 0;
	w = 0;

	while(w < y) {
		z += x;
		w += 1;
	}
	//@ assert(z == x * y);
	return 0;
}