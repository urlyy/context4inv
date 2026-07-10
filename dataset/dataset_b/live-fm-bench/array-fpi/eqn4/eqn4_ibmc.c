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

#define FORALL(Var, Type, Cond)       \
  Type Var;                           \
  __invariant(__forall(Var, Cond));   \

#define EXISTS(Var, Type, Cond)       \
  Type Var;                           \
  __invariant(__exists(Var, Cond));   \

int __VERIFIER_nondet_int();

int abs(int x){
  return x < 0 ? -x : x;
}

int main(int N, int *a, int *b)
{
	if(N > 0){
		__VERIFIER_assume(N <= 2147483647/4);
		int i = __VERIFIER_nondet_int();
		a[0] = 8;
		b[0] = 1;
		for(i=1; i<N; i++)
		{
			a[i] = a[i-1] + 8;
		}
		for(i=1; i<N; i++)
		{
			b[i] = b[i-1] + a[i-1];
		}
		int j;
		__VERIFIER_assert( __forall((void*)(&j), (!(0 <= j && j < N) || ((b[j] == 4*j*j + 4*j + 1)))) );
	}
	return 1;
}
