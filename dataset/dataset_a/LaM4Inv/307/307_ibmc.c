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

//svcomp_sumt3
int main(){
    unsigned int n = __VERIFIER_nondet_int();
    unsigned int j = __VERIFIER_nondet_int();
    unsigned int i = __VERIFIER_nondet_int();
    unsigned int k = __VERIFIER_nondet_int();
    unsigned int l = __VERIFIER_nondet_int();

    //pre-condition
    i = 0;
    k = 0;
    j = 0;
    l = 0;
    __ESBMC_assume((n <= 20000001));

    //loop-body
    while (l < n) {
        if ((l % 3) == 0) {
            i = i + 1;
        }
        else if((l % 2) == 0){
            j = j + 1;
        }
        else{
            k = k + 1;
        }
        l = l + 1;
    }

    //post-condition
    __VERIFIER_assert(((i + j + k) == l));
}