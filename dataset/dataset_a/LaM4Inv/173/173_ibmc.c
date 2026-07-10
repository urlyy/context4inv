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

//SyGuG2018_fib_25n
int main(){
    int x = __VERIFIER_nondet_int();
    int y = __VERIFIER_nondet_int();
    int i = __VERIFIER_nondet_int();
    int j = __VERIFIER_nondet_int();
    int turn = __VERIFIER_nondet_int();

    //pre-condition
    x = 0;
    y = 0;
    i = 0;
    j = 0;
    turn = 0;

    //loop-body
    while((turn >= 0) && (turn < 3)){
        if(turn == 0){
            if(__VERIFIER_nondet_int()){
                turn = 1;
            }
            else{
                turn = 2;
            }
        }
        else if(turn == 1 && x == y){
            if (x == y)
                i = i + 1;
            else{
                j = j + 1;
            }
            if(__VERIFIER_nondet_int()){
                turn = 1;
            }
            else{
                turn = 2;
            }
        }
        else if(turn == 2 && i >= j){
            if(i >= j)
                x = x + 1;
            y = y + 1;
            turn = 0;
        }
    }

    //post-condition
    __VERIFIER_assert((i >= j));
}