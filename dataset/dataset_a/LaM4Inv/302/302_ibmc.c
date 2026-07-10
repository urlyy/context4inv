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

//svcomp_loopv3
int main(){
    int i = __VERIFIER_nondet_int();
    int j = __VERIFIER_nondet_int();

    //pre-condition
    i = 0;

    //loop-body
    while(i < 50000001){  
        if(__VERIFIER_nondet_int())
            i = i + 8;
        else
            i = i + 4;
    }

    //post-condition
    if((j == (i / 4))){__VERIFIER_assert(((j * 4) == i));}
}