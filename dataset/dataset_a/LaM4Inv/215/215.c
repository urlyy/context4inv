//SyGuG2018_bk-nat
int main() {
    int invalid;
    int unowned;
    int nonexclusive;
    int exclusive;
    int RETURN;

    unowned = 0;
    nonexclusive = 0;
    exclusive = 0;
    //@ assume(invalid >= 1);
    int unknown1, unknown2;
    while(!((nonexclusive + unowned) >= 1 && invalid >= 1)) {
        if(invalid >= 1){
            if(unknown1!=0){
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
            unknown1 = unknown2;
        }
        else if((nonexclusive + unowned) >= 1){
            invalid = invalid + unowned + nonexclusive - 1;
            nonexclusive = 0;
            exclusive = exclusive + 1;
            unowned = 0;
        }
    }
    //@ assert(((nonexclusive + unowned) >= 1 && invalid >= 1)=>(invalid >= 0))
}