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

//SyGuG2018_fib_33ns
int main(){
    int x = __VERIFIER_nondet_int();
    int y = __VERIFIER_nondet_int();
    int z = __VERIFIER_nondet_int();
    int c = __VERIFIER_nondet_int();
    int k = __VERIFIER_nondet_int();
    int turn = __VERIFIER_nondet_int();

    //pre-condition
    x = 0;
    y = 0;
    turn = 0;
    __ESBMC_assume((z == k));

    //loop-body
    while(__VERIFIER_nondet_int()){
        if(turn == 0){
            c = 0;
            if(__VERIFIER_nondet_int()){
                turn = 1;
            }
            else{
                turn = 2;
            }
        }
        else if(turn == 1){
            if(z == (k + y - c)){
                y = y + 1;
                x = x + 1;
                c = c + 1;
                turn = 2;
            }
            else{
                y = y - 1;
                x = x + 1;
                c = c + 1;
                if(__VERIFIER_nondet_int()){
                    turn = 2;
                }
            }
        }
        else if(turn == 2){
            x = x - 1;
            y = y - 1;
            if(__VERIFIER_nondet_int()){
                turn = 3;
            }
        }
        else if(turn > 2 || turn < 0){
            z = x + y;
            turn = 0;
        }
    }

    //post-condition
    __VERIFIER_assert((x == y));
}