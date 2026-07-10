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

//SyGuG2018_fib_13
int main(){
    int j = __VERIFIER_nondet_int();
    int k = __VERIFIER_nondet_int();
    int t = __VERIFIER_nondet_int();

    //pre-condition
    j = 2;
    k = 0;

    //loop-body
    while(__VERIFIER_nondet_int()){
        if (t == 0){
            j = j + 4;
        }
        else {
            j = j + 2;
            k = k + 1;
        }
    }

    //post-condition
    if((k != 0)){__VERIFIER_assert((t != 0 && j == k * 2 + 2));}
}
