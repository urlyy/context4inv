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

int main(int CELLCOUNT)
{
	if(CELLCOUNT > 1 && CELLCOUNT %3 == 0)
	{
		int MINVAL=2;
		int i = __VERIFIER_nondet_int();
		int volArray[CELLCOUNT];
		int CCCELVOL3 = 7;
		int CCCELVOL2 = 3;
		int CCCELVOL1 = 1;
		for(i = 1; i <= CELLCOUNT/3; i++)
		{
			if(CCCELVOL3 >= MINVAL)
			{
				volArray[i*3 - 3] = CCCELVOL3;
			}
			else
			{
				volArray[i*3 - 3] = 0;
			}
			volArray[i*3 - 2] = volArray[i*3 - 2];
			volArray[i*3 - 1] = volArray[i*3 - 1];
		}
		for(i = 1; i <= CELLCOUNT/3; i++)
		{
			if(CCCELVOL2 >= MINVAL)
			{
				volArray[i*3 - 2] = CCCELVOL2;
			}
			else
			{
				volArray[i*3 - 2] = 0;
			}
			volArray[i*3 - 3] = volArray[i*3 - 3];
			volArray[i*3 - 1] = volArray[i*3 - 1];
		}
		for(i = 1; i <= CELLCOUNT/3; i++)
		{
			if(CCCELVOL1 >= MINVAL)
			{
				volArray[i*3 - 1] = CCCELVOL1;
			}
			else
			{
				volArray[i*3 - 1] = 0;
			}
			volArray[i*3 - 2] = volArray[i*3 - 2];
			volArray[i*3 - 3] = volArray[i*3 - 3];
		}
		int k;
		__VERIFIER_assert(__forall((void*)(&k), (!(k >= 0 && k < CELLCOUNT) || ((volArray[k] >= MINVAL || volArray[k] == 0)))));
	}
	return 1;
}
