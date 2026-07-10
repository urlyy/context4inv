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

//svcomp_eq2
int main(){
    int w = __VERIFIER_nondet_int();
    int x = __VERIFIER_nondet_int();
    int y = __VERIFIER_nondet_int();
    int z = __VERIFIER_nondet_int();

    //pre-condition
    x = w;
    z = x + 1;
    y = w + 1;
    __ESBMC_assume((x > 0));
    __ESBMC_assume((y > 0));
    __ESBMC_assume((z > 0));
    __ESBMC_assume((w > 0));

    //loop-body
    while(__VERIFIER_nondet_int()){
        y = y + 1;
        z = z + 1;
    }

    //post-conditon
    __VERIFIER_assert((y == z));
}
