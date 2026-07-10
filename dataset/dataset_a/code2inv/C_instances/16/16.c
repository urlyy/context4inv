

int main(int n)
{
    int x = 0;
    int m = 0;
    int unknown1, unknown2;
    while (x < n) {
        if (unknown1!=0) {
            m = x;
        }
        x = x + 1;
        unknown1 = unknown2;
    }
    //@ assert( (n > 0)=>(m >= 0) )
}
