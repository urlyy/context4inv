(set-logic LIA)

( declare-const i Int )
( declare-const i! Int )
( declare-const j Int )
( declare-const j! Int )
( declare-const k Int )
( declare-const k! Int )
( declare-const unknown1 Int )
( declare-const unknown1! Int )
( declare-const unknown2 Int )
( declare-const unknown2! Int )

( declare-const i_0 Int )
( declare-const i_1 Int )
( declare-const i_2 Int )
( declare-const i_3 Int )
( declare-const j_0 Int )
( declare-const j_1 Int )
( declare-const j_2 Int )
( declare-const j_3 Int )
( declare-const k_0 Int )
( declare-const k_1 Int )
( declare-const k_2 Int )
( declare-const unknown1_0 Int )
( declare-const unknown1_1 Int )
( declare-const unknown1_2 Int )
( declare-const unknown2_0 Int )

( define-fun inv-f( ( i Int )( j Int )( k Int )( unknown1 Int )( unknown2 Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( i Int )( j Int )( k Int )( unknown1 Int )( unknown2 Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int )( j_0 Int )( j_1 Int )( j_2 Int )( j_3 Int )( k_0 Int )( k_1 Int )( k_2 Int )( unknown1_0 Int )( unknown1_1 Int )( unknown1_2 Int )( unknown2_0 Int ) ) Bool
	( and
		( = i i_1 )
		( = j j_1 )
		( = k k_0 )
		( = i_1 1 )
		( = j_1 1 )
		( >= k_0 0 )
		( <= k_0 1 )
	)
)

( define-fun trans-f ( ( i Int )( j Int )( k Int )( unknown1 Int )( unknown2 Int )( i! Int )( j! Int )( k! Int )( unknown1! Int )( unknown2! Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int )( j_0 Int )( j_1 Int )( j_2 Int )( j_3 Int )( k_0 Int )( k_1 Int )( k_2 Int )( unknown1_0 Int )( unknown1_1 Int )( unknown1_2 Int )( unknown2_0 Int ) ) Bool
	( or
		( and
			( = i_2 i )
			( = j_2 j )
			( = k_1 k )
			( = unknown1_1 unknown1 )
			( = i_2 i! )
			( = j_2 j! )
			( = k_1 k! )
			( = unknown1_1 unknown1! )
			( = i i! )
			( = j j! )
			( = k k! )
			( = unknown2 unknown2! )
		)
		( and
			( = i_2 i )
			( = j_2 j )
			( = k_1 k )
			( = unknown1_1 unknown1 )
			( not ( = unknown1_1 0 ) )
			( = unknown1_2 unknown2_0 )
			( = i_3 ( + i_2 1 ) )
			( = j_3 ( + j_2 k_1 ) )
			( = k_2 ( - k_1 1 ) )
			( = i_3 i! )
			( = j_3 j! )
			( = k_2 k! )
			( = unknown1_2 unknown1! )
			(= unknown2 unknown2_0 )
			(= unknown2! unknown2_0 )
		)
	)
)

( define-fun post-f ( ( i Int )( j Int )( k Int )( unknown1 Int )( unknown2 Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int )( j_0 Int )( j_1 Int )( j_2 Int )( j_3 Int )( k_0 Int )( k_1 Int )( k_2 Int )( unknown1_0 Int )( unknown1_1 Int )( unknown1_2 Int )( unknown2_0 Int ) ) Bool
	( or
		( not
			( and
				( = i i_2)
				( = j j_2)
				( = k k_1)
				( = unknown1 unknown1_1)
				( = unknown2 unknown2_0 )
			)
		)
		( not
			( and
				( not ( not ( = unknown1_1 0 ) ) )
				( not ( >= i_2 1 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f i j k unknown1 unknown2 i_0 i_1 i_2 i_3 j_0 j_1 j_2 j_3 k_0 k_1 k_2 unknown1_0 unknown1_1 unknown1_2 unknown2_0  )
		( inv-f i j k unknown1 unknown2 )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f i j k unknown1 unknown2 )
			( trans-f i j k unknown1 unknown2 i! j! k! unknown1! unknown2! i_0 i_1 i_2 i_3 j_0 j_1 j_2 j_3 k_0 k_1 k_2 unknown1_0 unknown1_1 unknown1_2 unknown2_0 )
		)
		( inv-f i! j! k! unknown1! unknown2! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f i j k unknown1 unknown2  )
		( post-f i j k unknown1 unknown2 i_0 i_1 i_2 i_3 j_0 j_1 j_2 j_3 k_0 k_1 k_2 unknown1_0 unknown1_1 unknown1_2 unknown2_0 )
	)
))

