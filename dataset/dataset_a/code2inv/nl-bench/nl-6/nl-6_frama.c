/*@ ensures \result == 1; */
int unknown1();

/*@ ensures \result >= 1; */
int unknown2();

int main() {
	int x = unknown1();
	int y = unknown2();
	int z, w;

	w = 1;
	z = 1;

	while(x <= y)
	{
		w = w * x;
		if (x < y) {
			z = z * x;
		}
		x += 1;
	}
	//@ assert(w == z * y);
	return 0;
}