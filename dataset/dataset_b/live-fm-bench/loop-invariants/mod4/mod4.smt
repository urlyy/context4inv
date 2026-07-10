(set-logic LIA)

( declare-const x Int )
( declare-const x! Int )
( declare-const tmp Int )
( declare-const tmp! Int )

( declare-const x_0 Int )
( declare-const x_1 Int )

( define-fun inv-f( ( x Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( x Int )( tmp Int )( x_0 Int )( x_1 Int ) ) Bool
	( and
		( = x x_0 )
		( = x_0 0 )
	)
)

( define-fun trans-f ( ( x Int )( tmp Int )( x! Int )( tmp! Int )( x_0 Int )( x_1 Int ) ) Bool
	( or
		( and
			( = x x! )
			(= tmp tmp! )
		)
		( and
			(= x x_0 )
			(= x! x_0 )
			(= tmp tmp! )
		)
	)
)

( define-fun post-f ( ( x Int )( tmp Int )( x_0 Int )( x_1 Int ) ) Bool
	( or
		( not
			( = x x_0)
		)
		( not
			( and
				( not ( = ( mod x_0 4 ) 0 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f x tmp x_0 x_1  )
		( inv-f x tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f x tmp )
			( trans-f x tmp x! tmp! x_0 x_1 )
		)
		( inv-f x! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f x tmp  )
		( post-f x tmp x_0 x_1 )
	)
))

