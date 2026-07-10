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

int main()
{
int i = __VERIFIER_nondet_int(), j = __VERIFIER_nondet_int(), n = __VERIFIER_nondet_int();
  __VERIFIER_assume(n < 100000);
  __VERIFIER_assume(j>0 && j < 10000);
  int a[n];
  int k;
  for(i=1;i<n;i++) {
    int unknown1 = __VERIFIER_nondet_int();
    __VERIFIER_assume(unknown1>0 && unknown1 < 10000);
    a[i]=i+j+unknown1;
  }
  __VERIFIER_assert(__forall((void*)(&k), (!(1<=k && k<n) || ((a[k]>=(i+2))))));
  return 0;
}  
