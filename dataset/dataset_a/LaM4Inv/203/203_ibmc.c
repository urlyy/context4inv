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

//SyGuG2018_mirror2
int main(){
    int x = __VERIFIER_nondet_int();
    int y = __VERIFIER_nondet_int();

    //pre-condition
    __ESBMC_assume((x <= 1));
    __ESBMC_assume((x >= 0));
    y = -3;
    //loop-body
    while(__VERIFIER_nondet_int()){
        if(x - y < 2){
            x = x - 1;
            y = y + 2;
        }
        else if(x - y >= 2){
            y = y + 1;
        }
    }

    //post-condition
    __VERIFIER_assert((x <= 1));
    
}