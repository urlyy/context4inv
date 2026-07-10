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

//SyGuG2018_fib_09s
int main(){
    int i = __VERIFIER_nondet_int();
    int pvlen = __VERIFIER_nondet_int();
    int t = __VERIFIER_nondet_int();
    int k = __VERIFIER_nondet_int();
    int n = __VERIFIER_nondet_int();
    int j = __VERIFIER_nondet_int();
    int turn = __VERIFIER_nondet_int();

    //pre-condition
    k = 0;
    i = 0;
    turn = 0;

    //loop-body
    while(turn < 5){
        if(turn == 0){
            i = i + 1;
            if(__VERIFIER_nondet_int())){
                turn = 1;
            }
        }
        else if(turn == 1){
            if(i > pvlen){
                pvlen = i;
            }
            i = 0;
            turn = 2;
        }
        else if(turn == 2){
            t = i;
            i = i + 1;
            k = k + 1;
            if(__VERIFIER_nondet_int()){
                turn = 3;
            }
        }
        else if(turn == 3){
            if(__VERIFIER_nondet_int()){
                turn = 4;
            }
        }
        else if(turn == 4){
            n = i;
            j = 0;
            turn = 5;
        }
    }

    //post-condition
    __VERIFIER_assert((k >= 0));
}