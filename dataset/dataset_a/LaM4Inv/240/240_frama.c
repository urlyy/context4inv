//svcomp_loop1-1
/*@ ensures \result > -1.0 && \result < 1.0; */
float unknown1();

void foo() {
    float x = unknown1();
    float exp;
    float term;
    float result;
    unsigned int count;

    //pre-condition
    exp = 1.0;
    term = 1.0;
    count = 1;
    result = 2 * (1 / (1 - x));

    //loop-body
    while(unknown()){
        term = term * (x / count) ; 
		exp = exp + term ;
		count++ ;
    }

    //post-condition
    //@ assert(result >= exp);
}