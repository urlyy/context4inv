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
( declare-const y_0 Int )
( declare-const z_0 Int )
( declare-const z_1 Int )
( declare-const z_2 Int )
( declare-const z_3 Int )

( define-fun inv-f( ( x Int )( y Int )( z Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( x Int )( y Int )( z Int )( x_0 Int )( x_1 Int )( x_2 Int )( y_0 Int )( z_0 Int )( z_1 Int )( z_2 Int )( z_3 Int ) ) Bool
	( and
		( = x x_0 )
		( = y y_0 )
		( = z z_0 )
		( = x_0 0 )
		( = y_0 10000000 )
		( = z_0 5000000 )
	)
)

( define-fun trans-f ( ( x Int )( y Int )( z Int )( x! Int )( y! Int )( z! Int )( x_0 Int )( x_1 Int )( x_2 Int )( y_0 Int )( z_0 Int )( z_1 Int )( z_2 Int )( z_3 Int ) ) Bool
	( or
		( and
			( = x_1 x )
			( = z_1 z )
			( = x_1 x! )
			( = z_1 z! )
			( = y y_0 )
			( = y! y_0 )
			( = z z! )
		)
		( and
			( = x_1 x )
			( = z_1 z )
			( < x_1 y_0 )
			( >= x_1 5000000 )
			( = z_2 ( + z_1 1 ) )
			( = z_3 z_2 )
			( = x_2 ( + x_1 1 ) )
			( = x_2 x! )
			( = z_3 z! )
			(= y y_0 )
			(= y! y_0 )
		)
		( and
			( = x_1 x )
			( = z_1 z )
			( < x_1 y_0 )
			( not ( >= x_1 5000000 ) )
			( = z_3 z_1 )
			( = x_2 ( + x_1 1 ) )
			( = x_2 x! )
			( = z_3 z! )
			(= y y_0 )
			(= y! y_0 )
		)
	)
)

( define-fun post-f ( ( x Int )( y Int )( z Int )( x_0 Int )( x_1 Int )( x_2 Int )( y_0 Int )( z_0 Int )( z_1 Int )( z_2 Int )( z_3 Int ) ) Bool
	( or
		( not
			( and
				( = x x_1)
				( = y y_0)
				( = z z_1)
			)
		)
		( not
			( and
				( not ( < x_1 y_0 ) )
				( not ( = z_1 x_1 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f x y z x_0 x_1 x_2 y_0 z_0 z_1 z_2 z_3  )
		( inv-f x y z )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f x y z )
			( trans-f x y z x! y! z! x_0 x_1 x_2 y_0 z_0 z_1 z_2 z_3 )
		)
		( inv-f x! y! z! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f x y z  )
		( post-f x y z x_0 x_1 x_2 y_0 z_0 z_1 z_2 z_3 )
	)
))

