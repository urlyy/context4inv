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

//SyGuG2018_hhk2008_true-unreach-call_true-termination
int main(){
    int a = __VERIFIER_nondet_int();
    int b = __VERIFIER_nondet_int();
    int res = __VERIFIER_nondet_int();
    int cnt = __VERIFIER_nondet_int();

    //pre-condition
    res = a;
    cnt = b;
    __ESBMC_assume((a <= 1000000));
    __ESBMC_assume((b >= 0));
    __ESBMC_assume((b <= 1000000));

    //loop-body
    while(cnt > 0){
        cnt = cnt - 1;
        res = res + 1;
    }

    //post-condition
    __VERIFIER_assert((res == a + b));
        
}