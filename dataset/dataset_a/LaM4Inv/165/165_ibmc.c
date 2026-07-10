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

//SyGuG2018_fib_19
int main(){
    int n = __VERIFIER_nondet_int();
    int m = __VERIFIER_nondet_int();
    int x = __VERIFIER_nondet_int();
    int y = __VERIFIER_nondet_int();

    //pre-condition
    x = 0;
    y = m;
    __ESBMC_assume((n >= 0));
    __ESBMC_assume((m >= 0));
    __ESBMC_assume((m < n));

    //loop-body
    while(x < n){
        if(x + 1 <= m){
            x = x + 1;
        }
        else if (x + 1 > m){
            x = x + 1;
            y = y + 1;
        }
    }

    //post-condition
    if((x >= n)){__VERIFIER_assert((y == n));}
}