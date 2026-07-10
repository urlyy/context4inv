(set-logic LIA)

( declare-const SIZE Int )
( declare-const SIZE! Int )
( declare-const i Int )
( declare-const i! Int )
( declare-const j Int )
( declare-const j! Int )
( declare-const k Int )
( declare-const k! Int )
( declare-const n Int )
( declare-const n! Int )

( declare-const SIZE_0 Int )
( declare-const i_0 Int )
( declare-const i_1 Int )
( declare-const i_2 Int )
( declare-const i_3 Int )
( declare-const i_4 Int )
( declare-const j_0 Int )
( declare-const j_1 Int )
( declare-const j_2 Int )
( declare-const j_3 Int )
( declare-const j_4 Int )
( declare-const j_5 Int )
( declare-const j_6 Int )
( declare-const k_0 Int )
( declare-const k_1 Int )
( declare-const k_2 Int )
( declare-const k_3 Int )
( declare-const k_4 Int )
( declare-const n_0 Int )

( define-fun inv-f( ( SIZE Int )( i Int )( j Int )( k Int )( n Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( SIZE Int )( i Int )( j Int )( k Int )( n Int )( SIZE_0 Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int )( i_4 Int )( j_0 Int )( j_1 Int )( j_2 Int )( j_3 Int )( j_4 Int )( j_5 Int )( j_6 Int )( k_0 Int )( k_1 Int )( k_2 Int )( k_3 Int )( k_4 Int )( n_0 Int ) ) Bool
	( or
		( and
			( = SIZE SIZE_0 )
			( = i i_3 )
			( = j j_3 )
			( = n n_0 )
			( = SIZE_0 50000001 )
			( <= n_0 SIZE_0 )
			( = i_1 0 )
			( = j_1 0 )
			( = i_2 i_1 )
			( = j_2 j_1 )
			( < i_2 n_0 )
			( = i_3 ( + i_2 4 ) )
			( = j_3 ( + i_3 2 ) )
		)
		( and
			( = SIZE SIZE_0 )
			( = i i_2 )
			( = j j_2 )
			( = k k_1 )
			( = n n_0 )
			( = SIZE_0 50000001 )
			( <= n_0 SIZE_0 )
			( = i_1 0 )
			( = j_1 0 )
			( = i_2 i_1 )
			( = j_2 j_1 )
			( not ( < i_2 n_0 ) )
			( = k_1 i_2 )
		)
	)
)

( define-fun trans-f ( ( SIZE Int )( i Int )( j Int )( k Int )( n Int )( SIZE! Int )( i! Int )( j! Int )( k! Int )( n! Int )( SIZE_0 Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int )( i_4 Int )( j_0 Int )( j_1 Int )( j_2 Int )( j_3 Int )( j_4 Int )( j_5 Int )( j_6 Int )( k_0 Int )( k_1 Int )( k_2 Int )( k_3 Int )( k_4 Int )( n_0 Int ) ) Bool
	( or
		( and
			( = j_4 j )
			( = k_2 k )
			( = j_4 j! )
			( = k_2 k! )
			( = SIZE SIZE! )
			( = i i! )
			( = k k! )
			( = n n! )
		)
		( and
			( = j_4 j )
			( = k_2 k )
			( = ( mod j_4 2 ) 0 )
			( = j_5 ( - j_4 4 ) )
			( = k_3 ( - k_2 4 ) )
			( = j_5 j! )
			( = k_3 k! )
			(= SIZE SIZE_0 )
			(= SIZE! SIZE_0 )
			(= i i_3 )
			(= i! i_3 )
			(= n n_0 )
			(= n! n_0 )
		)
	)
)

( define-fun post-f ( ( SIZE Int )( i Int )( j Int )( k Int )( n Int )( SIZE_0 Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int )( i_4 Int )( j_0 Int )( j_1 Int )( j_2 Int )( j_3 Int )( j_4 Int )( j_5 Int )( j_6 Int )( k_0 Int )( k_1 Int )( k_2 Int )( k_3 Int )( k_4 Int )( n_0 Int ) ) Bool
	( or
		( not
			( and
				( = SIZE SIZE_0)
				( = i i_3)
				( = j j_4)
				( = k k_2)
				( = n n_0)
			)
		)
		( not
			( and
				( not ( = ( mod j_4 2 ) 0 ) )
				( not ( = ( mod k_2 2 ) 0 ) )
				( = i_4 i_0 )
				( = j_6 j_4 )
				( = k_4 k_2 )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f SIZE i j k n SIZE_0 i_0 i_1 i_2 i_3 i_4 j_0 j_1 j_2 j_3 j_4 j_5 j_6 k_0 k_1 k_2 k_3 k_4 n_0  )
		( inv-f SIZE i j k n )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f SIZE i j k n )
			( trans-f SIZE i j k n SIZE! i! j! k! n! SIZE_0 i_0 i_1 i_2 i_3 i_4 j_0 j_1 j_2 j_3 j_4 j_5 j_6 k_0 k_1 k_2 k_3 k_4 n_0 )
		)
		( inv-f SIZE! i! j! k! n! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f SIZE i j k n  )
		( post-f SIZE i j k n SIZE_0 i_0 i_1 i_2 i_3 i_4 j_0 j_1 j_2 j_3 j_4 j_5 j_6 k_0 k_1 k_2 k_3 k_4 n_0 )
	)
))

