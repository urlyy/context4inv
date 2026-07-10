//svcomp_id_trans

/*@
    requires (nlen == idBitLength / 32);
    requires (idBitLength >= 0);
    requires (material_length >= 0);
*/
void foo(int idBitLength, int material_length, int nlen) {
    int j;
    int k;

    //pre-condition
    j = 0;

    //loop-body
    while((j < idBitLength / 8) && (j < material_length)){
       j = j + 1;
    }

    //post-condition
    //@ assert(0 <= j);
}
