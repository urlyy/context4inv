
int main(int n)
{
    int x = 1;
    int m = 1;
    int unknown1, unknown2;
    while (x < n) {
        if (unknown1!=0) {
            m = x;
        }
        x = x + 1;
        unknown1= unknown2;
    }
    //@ assert((n > 1)=> (m < n))
}
