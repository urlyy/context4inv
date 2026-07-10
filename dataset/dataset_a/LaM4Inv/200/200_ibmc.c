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

//SyGuG2018_jmbl_trex3_vars
int main(){
    int x1 = __VERIFIER_nondet_int();
    int x2 = __VERIFIER_nondet_int();
    int x3 = __VERIFIER_nondet_int();
    int d1 = __VERIFIER_nondet_int();
    int d2 = __VERIFIER_nondet_int();
    int d3 = __VERIFIER_nondet_int();

    //pre-condition
    d1 = 1;
    d2 = 1;
    d2 = 1;

    //loop-body
    while(x1 > 0 && x2 > 0 && x3 > 0){
        if(__VERIFIER_nondet_int()){
            x1 = x1 - d1;
        }
        if(__VERIFIER_nondet_int()){
            x2 = x2 - d2;
        }
        if(__VERIFIER_nondet_int()){
            x3 = x3 - d3;
        }
    }

    //post-condition
    __VERIFIER_assert((x1 < 0 || x2 < 0 || x3 < 0 || x1 == 0 || x2 == 0 || x3 == 0));
    
}