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

//svcomp_nested-3
int main() {
    int last = __VERIFIER_nondet_int();
    int a = __VERIFIER_nondet_int();
    int b = __VERIFIER_nondet_int();
    int c = __VERIFIER_nondet_int();
    int st = __VERIFIER_nondet_int();

    //pre-condition
    a = 0;
    b = 0;
    c = 200000;
    __ESBMC_assume((st == 0 && last < c) || (st == 1 && last >= c));

    //loop-body
    while(__VERIFIER_nondet_int()){
        if(st == 0 && c == last + 1){
			a = a + 3; 
            b = b + 3;
        }
		else{	
            a = a + 2; 
            b = b + 2; 
        } 
		if(c == last && st == 0){
            a = a + 1;
            c = c + 1;
        } 
            
    }

    //post-condition
    __VERIFIER_assert((a == b));
}