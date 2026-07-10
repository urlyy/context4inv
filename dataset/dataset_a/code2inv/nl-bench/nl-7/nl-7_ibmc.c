extern void abort(void);
extern void __assert_fail(const char *, const char *, unsigned int, const char *) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__noreturn__));
void reach_error() { __assert_fail("0", "vnew2.c", 3, "reach_error"); }
extern void abort(void);
void assume_abort_if_not(int cond) {
  if(!cond) {abort();}
}
void __VERIFIER_assert(int cond) {
  if (!(cond)) {
    ERROR: {reach_error();abort();}
  }
  return;
}
int __VERIFIER_nondet_int();

int abs(int x){
  return x < 0 ? -x : x;
}

int main() {
	int x = __VERIFIER_nondet_int(), y = __VERIFIER_nondet_int(), z = __VERIFIER_nondet_int(), w = __VERIFIER_nondet_int();

	__ESBMC_assume(x >= 0 && y >= x);

	z = 0;
	w = 0;

	while(w < y) {
		z += x;
		w += 1;
	}

	__VERIFIER_assert((z == x * y));

	return 0;
}
