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

//SyGuG2018_cars
int main(){
    int x1 = __VERIFIER_nondet_int();
    int x2 = __VERIFIER_nondet_int();
    int x3 = __VERIFIER_nondet_int();
    int v1 = __VERIFIER_nondet_int();
    int v2 = __VERIFIER_nondet_int();
    int v3 = __VERIFIER_nondet_int();
    int t = __VERIFIER_nondet_int();

    //pre-condition
    x1 = 100;
    x2 = 75;
    x3 = -50;
    t = 0;
    __ESBMC_assume((v3 >= 0));
    __ESBMC_assume((v1 <= 5));
    __ESBMC_assume(((v1 - v3) >= 0));
    __ESBMC_assume((v2 * 2 - v1 - v3 == 0));
    __ESBMC_assume((v2 + 5 >= 0));
    __ESBMC_assume((v2 <= 5));

    //loop-body
    while(v2 + 5 >= 0 && v2 <= 5){
        x1 = x1 + v1;
        x3 = x3 + v3;
        x2 = x2 + v2;
        if(x2 * 2 - x1 - x3 >= 0){
            v2 = v2 - 1;
            
        }
        else if(x2 * 2 - x1 - x3 <= 0){
            v2 = v2 + 1;
        }
        t = t + 1;
    }

    //post-confition
    __VERIFIER_assert((v3 >= 0));
}
