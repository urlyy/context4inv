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

//svcomp_loop1-1
int main() {
    float x;
    float exp;
    float term;
    float result;
    unsigned int count = __VERIFIER_nondet_int();

    //pre-condition
    __ESBMC_assume((x > -1.0));
    __ESBMC_assume((x < 1.0));
    exp = 1.0;
    term = 1.0;
    count = 1;
    result = 2 * (1 / (1 - x));

    //loop-body
    while(__VERIFIER_nondet_int()){
        term = term * (x / count) ; 
		exp = exp + term ;
		count++ ;
    }

    //post-condition
    __VERIFIER_assert((result >= exp));
}