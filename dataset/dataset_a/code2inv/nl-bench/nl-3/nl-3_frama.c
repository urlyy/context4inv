/*@ ensures \result >= 0 && \result <= 10; */
int unknown1();

int main() {
	int x = unknown1();
	int y = x * x;

	while(x * x <= 1000) {
		x = x + 1;
		y = y + 1;
	}

	//@ assert(y <= 1000);
	return 0;
}