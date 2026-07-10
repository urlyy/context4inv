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

//SyGuG2018_cggmp2005_variant_true-unreach-call_true-termination
int main(){
    int lo = __VERIFIER_nondet_int();
    int mid = __VERIFIER_nondet_int();
    int hi = __VERIFIER_nondet_int();

    //pre-condition
    __ESBMC_assume((mid > 0));
    lo = 0;
    hi = 2 * mid;
    
    //loop-body
    while(mid > 0){
        lo = lo + 1;
        hi = hi - 1;
        mid = mid - 1;
    }

    //post-condition
    __VERIFIER_assert((lo == hi));
}