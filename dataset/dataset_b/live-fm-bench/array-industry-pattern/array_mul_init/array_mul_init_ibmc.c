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

int main(int *a, int *b)
{
	int SIZE=100000;
	int k = __VERIFIER_nondet_int();
	int i = __VERIFIER_nondet_int();
	for (i  = 0; i<SIZE ; i++)
	{
		a[i] = i; 
		b[i] = i ;
	}
int unknown1 = __VERIFIER_nondet_int(), unknown2 = __VERIFIER_nondet_int(), unknown3 = __VERIFIER_nondet_int();
	for (i=0; i< SIZE; i++)
	{
		if(unknown1!=0)
		{
			unknown1 = unknown2;
			a[i] = k;
			b[i] = k * k;
			k = unknown3;
		}
	}
	int j;
	__VERIFIER_assert( __forall((void*)(&j), (!(0 <= j && j < SIZE) || ((a[j] == b[j] || b[j] == a[j] * a[j])))) );
}
