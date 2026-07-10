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

//svcomp_loop2-1
int main() {
    float x;
	float octant;
	float oddExp;
	float evenExp;
	float term;
	unsigned int count = __VERIFIER_nondet_int();
	int multFactor = __VERIFIER_nondet_int();
	int temp = __VERIFIER_nondet_int();

    //pre-condition
    octant = 3.14159 / 3;
    __ESBMC_assume((x > 0));
    __ESBMC_assume((x < octant));
    oddExp = x;
    evenExp = 1.0;
    term = x;
    count = 2;
    multFactor = 0;

    //loop-body 
    while(__VERIFIER_nondet_int()){
		term = term * (x / count);
		
        if((count / 2) % 2 == 0){
            multFactor = 1;
        }else{
            multFactor = -1;
        }
		evenExp = evenExp + multFactor * term;

		count = count + 1;

		term = term * (x / count);		
		
		oddExp = oddExp + multFactor * term;
		
		count = count + 1;
	}

    //post-condition
	__VERIFIER_assert((oddExp >= evenExp));
}	