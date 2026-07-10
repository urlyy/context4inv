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
  int SIZE = 100000;
  int i = __VERIFIER_nondet_int();
  i = 1;
  a[0] = 7;
  int x;
  while( i < SIZE ) {
    a[i] = a[i-1] + 1;
    i = i + 1;
  }
  __VERIFIER_assert( __forall((void*)(&x), (!(1 <= x && x < SIZE) || ((a[x] >= a[x-1])))) );
  return 0;
}
int main(){return 0;}