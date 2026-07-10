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
( declare-const z_0 Int )

( define-fun inv-f( ( x Int )( y Int )( z Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( x Int )( y Int )( z Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( x_4 Int )( x_5 Int )( x_6 Int )( x_7 Int )( y_0 Int )( y_1 Int )( y_2 Int )( y_3 Int )( z_0 Int ) ) Bool
	( and
		( = x x_1 )
		( = y y_0 )
		( = z z_0 )
		( = x_0 0 )
		( = y_0 500000 )
		( = z_0 0 )
		( = x_1 0 )
	)
)

( define-fun trans-f ( ( x Int )( y Int )( z Int )( x! Int )( y! Int )( z! Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( x_4 Int )( x_5 Int )( x_6 Int )( x_7 Int )( y_0 Int )( y_1 Int )( y_2 Int )( y_3 Int )( z_0 Int ) ) Bool
	( or
		( and
			( = x_2 x )
			( = y_1 y )
			( = x_2 x! )
			( = y_1 y! )
			( = y y! )
			( = z z! )
		)
		( and
			( = x_2 x )
			( = y_1 y )
			( < x_2 1000000 )
			( < x_2 500000 )
			( = x_3 ( + x_2 1 ) )
			( = x_4 x_3 )
			( = y_2 y_1 )
			( = x_4 x! )
			( = y_2 y! )
			(= z z_0 )
			(= z! z_0 )
		)
		( and
			( = x_2 x )
			( = y_1 y )
			( < x_2 1000000 )
			( not ( < x_2 500000 ) )
			( < x_2 750000 )
			( = x_5 ( + x_2 1 ) )
			( = x_6 x_5 )
			( = y_3 ( + y_1 1 ) )
			( = x_4 x_6 )
			( = y_2 y_3 )
			( = x_4 x! )
			( = y_2 y! )
			(= z z_0 )
			(= z! z_0 )
		)
		( and
			( = x_2 x )
			( = y_1 y )
			( < x_2 1000000 )
			( not ( < x_2 500000 ) )
			( not ( < x_2 750000 ) )
			( = x_7 ( + x_2 2 ) )
			( = x_6 x_7 )
			( = y_3 ( + y_1 1 ) )
			( = x_4 x_6 )
			( = y_2 y_3 )
			( = x_4 x! )
			( = y_2 y! )
			(= z z_0 )
			(= z! z_0 )
		)
	)
)

( define-fun post-f ( ( x Int )( y Int )( z Int )( x_0 Int )( x_1 Int )( x_2 Int )( x_3 Int )( x_4 Int )( x_5 Int )( x_6 Int )( x_7 Int )( y_0 Int )( y_1 Int )( y_2 Int )( y_3 Int )( z_0 Int ) ) Bool
	( or
		( not
			( and
				( = x x_2)
				( = y y_1)
				( = z z_0)
			)
		)
		( not
			( and
				( not ( < x_2 1000000 ) )
				( not ( = x_2 1000000 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f x y z x_0 x_1 x_2 x_3 x_4 x_5 x_6 x_7 y_0 y_1 y_2 y_3 z_0  )
		( inv-f x y z )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f x y z )
			( trans-f x y z x! y! z! x_0 x_1 x_2 x_3 x_4 x_5 x_6 x_7 y_0 y_1 y_2 y_3 z_0 )
		)
		( inv-f x! y! z! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f x y z  )
		( post-f x y z x_0 x_1 x_2 x_3 x_4 x_5 x_6 x_7 y_0 y_1 y_2 y_3 z_0 )
	)
))

