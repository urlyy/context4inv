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

//SyGuG2018_ex1
int main(){
    int x = __VERIFIER_nondet_int();
    int y = __VERIFIER_nondet_int();
    int xa = __VERIFIER_nondet_int();
    int ya = __VERIFIER_nondet_int();

    //pre-condition
    xa = 0;
    ya = 0;

    //loop-body
    while(__VERIFIER_nondet_int()){
        x = xa + ya * 2 + 1;
        if(__VERIFIER_nondet_int()){
            y = ya - xa * 2 + x;
        }
        else{
            y = ya - xa * 2 - x;
        }
        xa = x - y * 2;
        ya = x * 2 + y;
    }
    
    //post-condtion
    __VERIFIER_assert((xa + ya * 2 >= 0));
}