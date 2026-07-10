/*@ ensures \result >= 0; */
int unknown1();

int main() {
	int x = unknown1();
	int y = x * x;
	while(unknown()) {
		x = x + 1;
		y = y + 1;
	}
	//@ assert(y <= x * x);
	return 0;
}