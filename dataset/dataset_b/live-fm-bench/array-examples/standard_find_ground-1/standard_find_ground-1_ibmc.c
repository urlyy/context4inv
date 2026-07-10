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

int foo( int *a) {
  int N=100000;
  int e = __VERIFIER_nondet_int();
  int i = 0;
  int j = __VERIFIER_nondet_int();
  int x;
  while( i < N && a[i] != e ) {
    i = i + 1;
  }
  __VERIFIER_assert( __forall((void*)(&x), (!(0 <= x && x < i) || ((a[x] != e)))) );
  return 0;
}

int main(){return 0;}