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

//SyGuG2018_fib_14
int main(){
    int a = __VERIFIER_nondet_int();
    int j = __VERIFIER_nondet_int();
    int m = __VERIFIER_nondet_int();

    //pre-condition
    a = 0;
    j = 1;
    __ESBMC_assume((m > 0));

    //loop-body
    while(j <= m){
        if(__VERIFIER_nondet_int()){
            a = a + 1;
        }
        else{
            a = a - 1;
        }
        j = j + 1;
    }

    //post-condition
    if((j > m)){__VERIFIER_assert((a <= m));}
}