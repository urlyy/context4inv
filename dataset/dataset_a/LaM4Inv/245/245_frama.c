//svcomp_nested-3
/*@
    requires c == 200000;
    requires (st == 0 && last < c) || (st == 1 && last >= c);
*/
void foo(int last,int st, int c) {
    int a;
    int b;

    //pre-condition
    a = 0;
    b = 0;

    //loop-body
    while(unknown()){
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
    //@ assert(c == 200000);
}