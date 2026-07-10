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

//svcomp_benchmark49_linear
int main(){
    int i = __VERIFIER_nondet_int();
    int j = __VERIFIER_nondet_int();
    int r = __VERIFIER_nondet_int();

    //pre-condition
    __ESBMC_assume((r > i + j));

    //loop-body
    while (i > 0) {
        i = i - 1;
        j = j + 1;
    }

    //post-condition
    __VERIFIER_assert((r > i + j));
}