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

int foo(int *a,int *b)
{
  int size = 10000;
  int i = 0;
  int j = 0;
  int k;
  while( i < size )
  {
	    a[j] = b[i];
      i = i+1;
      j = j+1;
  }
  __VERIFIER_assert( __forall((void*)(&k), (!(0 <= k && k < size) || ((a[k] == b[k])))) );
  return 0;
}
int main(){return 0;}