(set-logic LIA)

( declare-const x Int )
( declare-const x! Int )

( declare-const x_0 Int )
( declare-const x_1 Int )
( declare-const x_2 Int )
( declare-const x_3 Int )
( declare-const x_4 Int )

( define-fun inv-f( ( x Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( x Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( x_4 Int ) ) Bool
	( and
		( = x x_0 )
		( = x_0 0 )
	)
)

( define-fun trans-f ( ( x Int )( x! Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( x_4 Int ) ) Bool
	( or
		( and
			( = x_1 x )
			( = x_1 x! )
		)
		( and
			( = x_1 x )
			( < x_1 100000000 )
			( < x_1 10000000 )
			( = x_2 ( + x_1 1 ) )
			( = x_3 x_2 )
			( = x_3 x! )
		)
		( and
			( = x_1 x )
			( < x_1 100000000 )
			( not ( < x_1 10000000 ) )
			( = x_4 ( + x_1 2 ) )
			( = x_3 x_4 )
			( = x_3 x! )
		)
	)
)

( define-fun post-f ( ( x Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( x_4 Int ) ) Bool
	( or
		( not
			( = x x_1)
		)
		( not
			( and
				( not ( < x_1 100000000 ) )
				( not ( = x_1 100000000 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f x x_0 x_1 x_2 x_3 x_4  )
		( inv-f x )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f x )
			( trans-f x x! x_0 x_1 x_2 x_3 x_4 )
		)
		( inv-f x! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f x  )
		( post-f x x_0 x_1 x_2 x_3 x_4 )
	)
))

