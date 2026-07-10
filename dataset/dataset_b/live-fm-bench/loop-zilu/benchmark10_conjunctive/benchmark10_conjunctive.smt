(set-logic LIA)

( declare-const c Int )
( declare-const c! Int )
( declare-const i Int )
( declare-const i! Int )

( declare-const c_0 Int )
( declare-const c_1 Int )
( declare-const c_2 Int )
( declare-const c_3 Int )
( declare-const i_0 Int )
( declare-const i_1 Int )
( declare-const i_2 Int )
( declare-const i_3 Int )

( define-fun inv-f( ( c Int )( i Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( c Int )( i Int )( c_0 Int )( c_1 Int )( c_2 Int )( c_3 Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int ) ) Bool
	( or
		( and
			( = c c_0 )
			( = i i_0 )
			( = c_0 0 )
			( = i_0 0 )
		)
	)
)

( define-fun trans-f ( ( c Int )( i Int )( c! Int )( i! Int )( c_0 Int )( c_1 Int )( c_2 Int )( c_3 Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int ) ) Bool
	( or
		( and
			( = c_1 c )
			( = i_1 i )
			( = c_1 c! )
			( = i_1 i! )
			( = c c! )
		)
		( and
			( = c_1 c )
			( = i_1 i )
			( < i_1 100 )
			( > i_1 0 )
			( = c_2 ( + c_1 i_1 ) )
			( = i_2 ( + i_1 1 ) )
			( = c_2 c! )
			( = i_2 i! )
		)
		( and
			( < i_1 100 )
			( not ( > i_1 0 ) )
			(= c c_0 )
			(= c! c_0 )
			(= i i_0 )
			(= i! i_0 )
		)
	)
)

( define-fun post-f ( ( c Int )( i Int )( c_0 Int )( c_1 Int )( c_2 Int )( c_3 Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int ) ) Bool
	( or
		( not
			( and
				( = c c_1)
				( = i i_1)
			)
		)
		( not
			( and
				( not ( < i_1 100 ) )
				( not ( >= c_1 0 ) )
				( = c_3 c_1 )
				( = i_3 i_1 )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f c i c_0 c_1 c_2 c_3 i_0 i_1 i_2 i_3  )
		( inv-f c i )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f c i )
			( trans-f c i c! i! c_0 c_1 c_2 c_3 i_0 i_1 i_2 i_3 )
		)
		( inv-f c! i! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f c i  )
		( post-f c i c_0 c_1 c_2 c_3 i_0 i_1 i_2 i_3 )
	)
))

