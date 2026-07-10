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

int main(int i,int j,int x,int y,int k) {
  j=0;
  if ((x+y==k)){
int unknown1 = __VERIFIER_nondet_int(), unknown2 = __VERIFIER_nondet_int();
    while (unknown1!=0) {
      unknown1 = unknown2;
      if(j==i) {x++;y--;} else {y++;x--;} j++;
    }
    __VERIFIER_assert(x+y==k);
  }
  return 0;
}
