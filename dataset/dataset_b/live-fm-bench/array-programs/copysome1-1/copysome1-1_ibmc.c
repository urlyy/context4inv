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


int main(int *a1, int *a2) {
  int N=200000;
  int i = __VERIFIER_nondet_int(); 
  int z = __VERIFIER_nondet_int();
  z = 150000;
  for ( i = 0 ; i < N ; i++ ) {
      if (i != z){
        a2[i] = a1[i];
      }
  }
  int k;
  __VERIFIER_assert(__forall((void*)(&k), (!(k >= 0 && k < N && k != z) || ((a1[k] == a2[k])))));
  return 0;
}
