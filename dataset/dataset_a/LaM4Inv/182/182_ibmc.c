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
int __VERIFIER_nondet_int();

int abs(int x){
  return x < 0 ? -x : x;
}

//SyGuG2018_fib_41
int main(){
    int k = __VERIFIER_nondet_int();
    int n = __VERIFIER_nondet_int();
    int i = __VERIFIER_nondet_int();
    int j = __VERIFIER_nondet_int();

    //pre-condition
    j = 0;
    i = 0;
    __ESBMC_assume((n >= 0));
    __ESBMC_assume((n <= 20000001));
    __ESBMC_assume((k >= 0));
    __ESBMC_assume((k <= 20000001));

    //loop-body
    while(i <= n){
        i = i + 1;
        j = j + 1;
    }

    //post-condition
    if((i > n)){__VERIFIER_assert((k + i + j) > (2 * n));}
}