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

//SyGuG2018_fib_20
int main(){
    int x = __VERIFIER_nondet_int();
    int y = __VERIFIER_nondet_int();
    int k = __VERIFIER_nondet_int();
    int j = __VERIFIER_nondet_int();
    int i = __VERIFIER_nondet_int();
    int n = __VERIFIER_nondet_int();
    int m = __VERIFIER_nondet_int();

    //pre-condition
    m = 0;
    j = 0;
    __ESBMC_assume(((x + y) == k));

    //loop-body
    while(j < n){
        if(j == i){
            x = x + 1;
            y = y - 1;
            j = j + 1;
            if(__VERIFIER_nondet_int()){
                m = j;
            }
        }
        else if(j != i){
            x = x - 1;
            y = y + 1;
            j = j + 1;
            if(__VERIFIER_nondet_int()){
                m = j;
            }
        }

    }

    //post-condition
    if((j >= n && m > n)){__VERIFIER_assert((n <= 0));}
}