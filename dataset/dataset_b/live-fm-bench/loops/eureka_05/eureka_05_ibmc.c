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

int main(int *array){
   int SIZE = 5;
   int n = SIZE;
   int i = __VERIFIER_nondet_int();
	for(i=SIZE-1; i>=0; i--){
		array[i]=i;
   }
int lh = __VERIFIER_nondet_int(), rh = __VERIFIER_nondet_int(), i = __VERIFIER_nondet_int(), temp = __VERIFIER_nondet_int();
   for (lh = 0; lh < n; lh++) {
      rh = lh;
      for (i = lh + 1; i < n; i++){
         if (array[i] < array[rh]){
            rh = i;
         }
      }
      temp = array[lh];
      array[lh] = array[rh];
      array[rh] = temp;
   }
   int k;
	__VERIFIER_assert(__forall((void*)(&k), (!(k >= 0 && k < SIZE) || ((array[k] == k)))));
}
