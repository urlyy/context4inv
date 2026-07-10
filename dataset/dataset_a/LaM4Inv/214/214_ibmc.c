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

//SyGuG2018_bk-nat
int main() {
    int invalid = __VERIFIER_nondet_int();
    int unowned = __VERIFIER_nondet_int();
    int nonexclusive = __VERIFIER_nondet_int();
    int exclusive = __VERIFIER_nondet_int();
    int RETURN = __VERIFIER_nondet_int();

    unowned = 0;
    nonexclusive = 0;
    exclusive = 0;
    __ESBMC_assume((invalid >= 1));
    while(!((nonexclusive + unowned) >= 1 && invalid >= 1)) {
        if(invalid >= 1){
            if(__VERIFIER_nondet_int()){
                nonexclusive = nonexclusive + exclusive;
                exclusive = 0;
                invalid = invalid - 1;
                unowned = unowned + 1;
            }
            else{
                exclusive = 1;
                unowned = 0;
                nonexclusive = 0;
            }
        }
        else if((nonexclusive + unowned) >= 1){
            invalid = invalid + unowned + nonexclusive - 1;
            nonexclusive = 0;
            exclusive = exclusive + 1;
            unowned = 0;
        }
    }
    if(((nonexclusive + unowned) >= 1 && invalid >= 1)){__VERIFIER_assert((unowned >= 0));}
}