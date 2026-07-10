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

//svcomp_gauss_sum
int main(){
    int n = __VERIFIER_nondet_int();
    int sum = __VERIFIER_nondet_int();
    int i = __VERIFIER_nondet_int();

    //pre-condition
    __ESBMC_assume((n >= 1));
    __ESBMC_assume((n <= 1000));
    sum = 0;
    i = 0;

    //loop-body
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }

    //post-condition
    __VERIFIER_assert(2 * sum == n * (n - 1);
}
