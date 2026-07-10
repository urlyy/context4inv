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

//svcomp_Mono3_1
int main(){
    unsigned int x = __VERIFIER_nondet_int();
    unsigned int y = __VERIFIER_nondet_int();

    //pre-condition
    x = 0;
    y = 0;

    //loop-body
    while (x < 1000000) {
        if (x < 500000) {
	        y++;
        } 
        else {
	        y--;
        }
	    x++;
    }


    //post-condition
    __VERIFIER_assert((y == 0));
}