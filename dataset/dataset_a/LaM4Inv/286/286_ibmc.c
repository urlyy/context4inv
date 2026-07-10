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

//svcomp_benchmark42_conjunctive
int main(){
    int x = __VERIFIER_nondet_int();
    int y = __VERIFIER_nondet_int();
    int z = __VERIFIER_nondet_int();

    //pre-condition
    __ESBMC_assume((x == y));
    __ESBMC_assume((x >= 0));
    __ESBMC_assume((x + y + z == 0));

    //loop-body
    while (x > 0) {
        x--;
        y--;
        z += 2;
    }

    //post-condition
    __VERIFIER_assert((z <= 0));
}