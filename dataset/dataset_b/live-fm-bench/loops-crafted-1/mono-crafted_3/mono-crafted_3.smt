(set-logic LIA)

( declare-const x Int )
( declare-const x! Int )
( declare-const y Int )
( declare-const y! Int )
( declare-const z Int )
( declare-const z! Int )

( declare-const x_0 Int )
( declare-const x_1 Int )
( declare-const x_2 Int )
( declare-const x_3 Int )
( declare-const x_4 Int )
( declare-const x_5 Int )
( declare-const x_6 Int )
( declare-const x_7 Int )
( declare-const y_0 Int )
( declare-const y_1 Int )
( declare-const y_2 Int )
( declare-const y_3 Int )
( declare-const y_4 Int )
( declare-const y_5 Int )
( declare-const z_0 Int )
( declare-const z_1 Int )
( declare-const z_2 Int )

( define-fun inv-f( ( x Int )( y Int )( z Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( x Int )( y Int )( z Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( x_4 Int )( x_5 Int )( x_6 Int )( x_7 Int )( y_0 Int )( y_1 Int )( y_2 Int )( y_3 Int )( y_4 Int )( y_5 Int )( z_0 Int )( z_1 Int )( z_2 Int ) ) Bool
	( or
		( and
			( = x x_4 )
			( = y y_2 )
			( = z z_0 )
			( = x_0 0 )
			( = y_0 500000 )
			( = z_0 0 )
			( = x_1 0 )
			( = x_2 x_1 )
			( = y_1 y_0 )
			( < x_2 1000000 )
			( < x_2 500000 )
			( = x_3 ( + x_2 1 ) )
			( = x_4 x_3 )
			( = y_2 y_1 )
		)
		( and
			( = x x_4 )
			( = y y_2 )
			( = z z_0 )
			( = x_0 0 )
			( = y_0 500000 )
			( = z_0 0 )
			( = x_1 0 )
			( = x_2 x_1 )
			( = y_1 y_0 )
			( < x_2 1000000 )
			( not ( < x_2 500000 ) )
			( = x_5 ( + x_2 1 ) )
			( = y_3 ( + y_1 1 ) )
			( = x_4 x_5 )
			( = y_2 y_3 )
		)
		( and
			( = x x_2 )
			( = y y_1 )
			( = z z_0 )
			( = x_0 0 )
			( = y_0 500000 )
			( = z_0 0 )
			( = x_1 0 )
			( = x_2 x_1 )
			( = y_1 y_0 )
			( not ( < x_2 1000000 ) )
		)
	)
)

( define-fun trans-f ( ( x Int )( y Int )( z Int )( x! Int )( y! Int )( z! Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( x_4 Int )( x_5 Int )( x_6 Int )( x_7 Int )( y_0 Int )( y_1 Int )( y_2 Int )( y_3 Int )( y_4 Int )( y_5 Int )( z_0 Int )( z_1 Int )( z_2 Int ) ) Bool
	( or
		( and
			( = x_6 x )
			( = y_4 y )
			( = z_1 z )
			( = x_6 x! )
			( = y_4 y! )
			( = z_1 z! )
			( = x x! )
			( = z z! )
		)
		( and
			( = x_6 x )
			( = y_4 y )
			( = z_1 z )
			( > y_4 0 )
			( = x_7 ( - x_6 1 ) )
			( = z_2 ( + z_1 1 ) )
			( = y_5 ( - y_4 2 ) )
			( = x_7 x! )
			( = y_5 y! )
			( = z_2 z! )
		)
	)
)

( define-fun post-f ( ( x Int )( y Int )( z Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( x_4 Int )( x_5 Int )( x_6 Int )( x_7 Int )( y_0 Int )( y_1 Int )( y_2 Int )( y_3 Int )( y_4 Int )( y_5 Int )( z_0 Int )( z_1 Int )( z_2 Int ) ) Bool
	( or
		( not
			( and
				( = x x_6)
				( = y y_4)
				( = z z_1)
			)
		)
		( not
			( and
				( not ( > y_4 0 ) )
				( not ( = x_6 z_1 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f x y z x_0 x_1 x_2 x_3 x_4 x_5 x_6 x_7 y_0 y_1 y_2 y_3 y_4 y_5 z_0 z_1 z_2  )
		( inv-f x y z )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f x y z )
			( trans-f x y z x! y! z! x_0 x_1 x_2 x_3 x_4 x_5 x_6 x_7 y_0 y_1 y_2 y_3 y_4 y_5 z_0 z_1 z_2 )
		)
		( inv-f x! y! z! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f x y z  )
		( post-f x y z x_0 x_1 x_2 x_3 x_4 x_5 x_6 x_7 y_0 y_1 y_2 y_3 y_4 y_5 z_0 z_1 z_2 )
	)
))

