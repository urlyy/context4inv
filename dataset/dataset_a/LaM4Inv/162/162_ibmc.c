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

//SyGuG2018_fib_17n
int main(){
    int k = __VERIFIER_nondet_int();
    int i = __VERIFIER_nondet_int();
    int j = __VERIFIER_nondet_int();
    int n = __VERIFIER_nondet_int();
    int turn = __VERIFIER_nondet_int();

    //pre-condition
    k = 1;
    i = 1;
    j = 0;
    turn = 0;

    //loop-body
    while((turn >= 0) && (turn < 3)){
        if(turn == 0 && i >= n){
            turn = 3;
        }
        else if(turn == 1 && j < i){
            k = k + i - j;
            j = j + 1;
        }
        else if (turn == 1 && j >= i){
            turn = 2;
        }
        else if(turn == 2){
            i = i + 1;
            turn = 0;
        }
    }

    //post-condition
    if((turn == 3)){__VERIFIER_assert((k >= n));}
}