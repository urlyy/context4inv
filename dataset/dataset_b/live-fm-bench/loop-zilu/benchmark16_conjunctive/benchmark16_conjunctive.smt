(set-logic LIA)

( declare-const i Int )
( declare-const i! Int )
( declare-const k Int )
( declare-const k! Int )
( declare-const tmp Int )
( declare-const tmp! Int )

( declare-const i_0 Int )
( declare-const i_1 Int )
( declare-const i_2 Int )
( declare-const i_3 Int )
( declare-const k_0 Int )
( declare-const k_1 Int )
( declare-const k_2 Int )
( declare-const k_3 Int )

( define-fun inv-f( ( i Int )( k Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( i Int )( k Int )( tmp Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int )( k_0 Int )( k_1 Int )( k_2 Int )( k_3 Int ) ) Bool
	( or
		( and
			( = i i_0 )
			( = k k_0 )
			( <= 0 k_0 )
			( <= k_0 1 )
			( = i_0 1 )
		)
	)
)

( define-fun trans-f ( ( i Int )( k Int )( tmp Int )( i! Int )( k! Int )( tmp! Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int )( k_0 Int )( k_1 Int )( k_2 Int )( k_3 Int ) ) Bool
	( or
		( and
			( = i_1 i )
			( = k_1 k )
			( = i_1 i! )
			( = k_1 k! )
			( = i i! )
			( = k k! )
			(= tmp tmp! )
		)
		( and
			( = i_1 i )
			( = k_1 k )
			( = i_2 ( + i_1 1 ) )
			( = k_2 ( - k_1 1 ) )
			( = i_2 i! )
			( = k_2 k! )
			(= tmp tmp! )
		)
	)
)

( define-fun post-f ( ( i Int )( k Int )( tmp Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int )( k_0 Int )( k_1 Int )( k_2 Int )( k_3 Int ) ) Bool
	( and
		( or
			( not
				( and
					( = i i_1)
					( = k k_1)
				)
			)
			( not
				( and
					( <= 1 ( + i_1 k_1 ) )
					( <= ( + i_1 k_1 ) 2 )
					( not ( and ( and ( <= 1 ( + i_1 k_1 ) ) ( <= ( + i_1 k_1 ) 2 ) ) ( >= i_1 1 ) ) )
					( = i_3 i_1 )
					( = k_3 k_1 )
				)
			)
		)
		( or
			( not
				( and
					( = i i_1)
					( = k k_1)
				)
			)
			( not
				( and
					( <= 1 ( + i_1 k_1 ) )
					( not ( <= ( + i_1 k_1 ) 2 ) )
					( not ( and ( and ( <= 1 ( + i_1 k_1 ) ) ( <= ( + i_1 k_1 ) 2 ) ) ( >= i_1 1 ) ) )
					( = i_3 i_1 )
					( = k_3 k_1 )
				)
			)
		)
		( or
			( not
				( and
					( = i i_1)
					( = k k_1)
				)
			)
			( not
				( and
					( not ( <= 1 ( + i_1 k_1 ) ) )
					( not ( and ( and ( <= 1 ( + i_1 k_1 ) ) ( <= ( + i_1 k_1 ) 2 ) ) ( >= i_1 1 ) ) )
					( = i_3 i_1 )
					( = k_3 k_1 )
				)
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f i k tmp i_0 i_1 i_2 i_3 k_0 k_1 k_2 k_3  )
		( inv-f i k tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f i k tmp )
			( trans-f i k tmp i! k! tmp! i_0 i_1 i_2 i_3 k_0 k_1 k_2 k_3 )
		)
		( inv-f i! k! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f i k tmp  )
		( post-f i k tmp i_0 i_1 i_2 i_3 k_0 k_1 k_2 k_3 )
	)
))

