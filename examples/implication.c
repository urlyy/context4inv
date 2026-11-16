void count_down(int cl) {
    int p = 0;
    int c = cl;

    while (p < 4 && cl > 0) {
        cl -= 1;
        p += 1;
    }

    //@ assert((p != 4) => (c < 4))
}
