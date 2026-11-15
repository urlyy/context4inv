//SyGuG2018_brett
int main(){
    int p;
    int c;
    int cl;
    
    //pre-condition
    (p = 0);
    (c = cl);

    while(((p < 4) && (cl > 0))){
        (cl = cl - 1);
        (p = p + 1);
    }
    //@ assert((p != 4)=>(c < 4))
}