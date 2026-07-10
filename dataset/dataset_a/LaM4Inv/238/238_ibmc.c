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

//svcomp_simple_vardep_2
int main() {
    unsigned int i = __VERIFIER_nondet_int();
    unsigned int j = __VERIFIER_nondet_int();
    unsigned int k = __VERIFIER_nondet_int();

    //pre-condition
    i = 0;
    j = 0;
    k = 0;

    //loop-body
    while (k < 268435455) {
        i = i + 1;
        j = j + 2;
        k = k + 3;
    }

    //post-condition
    __VERIFIER_assert((k == 3 * i));
}