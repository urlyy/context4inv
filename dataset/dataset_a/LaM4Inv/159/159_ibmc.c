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

//SyGuG2018_fib_15
int main(){
    int n = __VERIFIER_nondet_int();
    int j = __VERIFIER_nondet_int();
    int k = __VERIFIER_nondet_int();

    //pre-condition
    j = 0;
    __ESBMC_assume((n > 0));
    __ESBMC_assume((k > n));

    //loop-body
    while(j < n){
        j = j + 1;
        k = k - 1;
    }

    //post-condition
    if((j >= n)){__VERIFIER_assert((k >= 0));}
}