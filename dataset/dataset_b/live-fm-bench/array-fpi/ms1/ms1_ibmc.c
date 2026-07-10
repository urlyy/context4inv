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

int main(int N, int *a)
{
	if(N > 0){
		__VERIFIER_assume(N <= 2147483647/4);
		int i = __VERIFIER_nondet_int();
		int sum[1];
		for(i=0; i<N; i++)
		{
			a[i] = i%1;
		}
		for(i=0; i<N; i++)
		{
			if(i==0) {
				sum[0] = 0;
			} else {
				sum[0] = sum[0] + a[i];
			}
		}
		__VERIFIER_assert(sum[0] == 0);
	}
	return 1;
}
