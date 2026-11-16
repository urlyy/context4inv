void count_to(int n) {
    int i = 0;
    //@ assume(n >= 0)
    while (i < n) {
        i++;
    }
    //@ assert(i == n)
}
