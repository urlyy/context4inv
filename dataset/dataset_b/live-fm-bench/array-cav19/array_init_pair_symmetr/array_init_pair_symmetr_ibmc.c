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
  int i = __VERIFIER_nondet_int();
  int N = 100000;
  int a[N];
  int b[N];
  int c[N];
  int k;  
  for(i=0;i<N;i++) {
    int unknown1;
    __VERIFIER_assume(unknown1 > -100000 && unknown1 < 100000);
    a[i]=unknown1;
    b[i]=0-unknown1;
  }
  for(i=0;i<N;i++){
    c[i]=a[i]+b[i];
  }
  
  __VERIFIER_assert(__forall((void*)(&k), (!(1<=k && k<N) || ((c[k] == 0)))));
  return 0;
}
