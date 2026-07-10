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

//svcomp_mod3
int main() {
    unsigned int x = __VERIFIER_nondet_int();
    unsigned int y = __VERIFIER_nondet_int();

    //pre-condition
    y = 1;

    //loop-body
    while(__VERIFIER_nondet_int()){
        if(x % 3 == 1){
            x = x + 2; 
            y = 0;
        }
        else{
            if(x % 3 == 2){
                x = x + 1; 
                y = 0;
            }
            else{
                if(__VERIFIER_nondet_int()){
                    x = x + 4; 
                    y = 1;
                }
                else{
                    x = x + 5; 
                    y = 1;
                }
            }
        }
    }

    //post-condition
    if((y == 0)){__VERIFIER_assert((x % 3 == 0));}
}