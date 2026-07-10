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

int foo(int *vectorx)
{
    int i = __VERIFIER_nondet_int();
    int n = 100000;
    int pos = __VERIFIER_nondet_int();
    int element = __VERIFIER_nondet_int();
    int found = 0;
    int x;
    for (i = 0; i < n && found!=0; i++)
    {
        if (vectorx[i] == element)
        {
            found = 1;
            pos = i;
        }
    }
    if ( found !=0 )
    {
        for (i = pos; i <  n - 1; i++)
        {
            vectorx[i] = vectorx[i + 1];
        }
        __VERIFIER_assert( !(found!=0) || __forall((void*)(&x), (!(0 <= x && x < pos) || ((vectorx[x] != element)))) );
    }
  return 0;
}

int main(){return 0;}