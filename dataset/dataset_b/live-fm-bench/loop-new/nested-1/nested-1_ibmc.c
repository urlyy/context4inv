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

int main(int n,int m) {
    int k = 0;
int i = __VERIFIER_nondet_int(), j = __VERIFIER_nondet_int();
    if (10 <= n && n <= 10000 && 10 <= m && m <= 10000){
        for (i = 0; i < n; i++) {
            for (j = 0; j < m; j++) {
                k ++;
            }
        }
        __VERIFIER_assert(k >= 100);
    }
    return 0;
}
