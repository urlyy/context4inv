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

#define FORALL(Var, Type, Cond)       \
  Type Var;                           \
  __invariant(__forall(Var, Cond));   \

#define EXISTS(Var, Type, Cond)       \
  Type Var;                           \
  __invariant(__exists(Var, Cond));   \

int __VERIFIER_nondet_int();

int abs(int x){
  return x < 0 ? -x : x;
}

int main() {
int n = __VERIFIER_nondet_int(), i = __VERIFIER_nondet_int(), j = __VERIFIER_nondet_int();
int unknown1 = __VERIFIER_nondet_int(), unknown2 = __VERIFIER_nondet_int(), unknown3 = __VERIFIER_nondet_int();
  n = unknown1;
  if(n <= 500000){
    i = 0; j=0;
    while(i<n){ 
      if(unknown2!=0){
        i = i + 6; 
      }else{
        i = i + 3; 
      }
      unknown2 = unknown3; 
    }
    __VERIFIER_assert( !(n <= 500000) || (i%3==0) );
  }
  
  return 0;
}
