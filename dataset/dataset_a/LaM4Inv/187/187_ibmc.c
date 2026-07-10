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

//SyGuG2018_gcnr_tacas08
int main(){
    int x = __VERIFIER_nondet_int();
    int y = __VERIFIER_nondet_int();
    int z = __VERIFIER_nondet_int();
    int w = __VERIFIER_nondet_int();

    //pre-condition
    x = 0;
    y = 0;
    z = 0;
    w = 0;

    //loop-body
    while(__VERIFIER_nondet_int()){
        if(x >= 4){
            x = x + 1;
            y = y + 2;
            
        }
        else if(y > 10 * w && z >= 100 * x){
            y = 0 - y;
        }
        else{
            x = x + 1;
            y = y + 100;
        }
        w = w + 1;
        z = z + 10;
    }

    //post-condition
    if((x >= 4)){__VERIFIER_assert((y > 2));}
        
}