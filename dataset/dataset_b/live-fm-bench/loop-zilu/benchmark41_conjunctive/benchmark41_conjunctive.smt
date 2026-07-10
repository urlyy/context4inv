(set-logic LIA)

( declare-const x Int )
( declare-const x! Int )
( declare-const y Int )
( declare-const y! Int )
( declare-const z Int )
( declare-const z! Int )
( declare-const tmp Int )
( declare-const tmp! Int )

( declare-const x_0 Int )
( declare-const y_0 Int )
( declare-const z_0 Int )
( declare-const z_1 Int )

( define-fun inv-f( ( x Int )( y Int )( z Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( x Int )( y Int )( z Int )( tmp Int )( x_0 Int )( y_0 Int )( z_0 Int )( z_1 Int ) ) Bool
	( or
		( and
			( = x x_0 )
			( = y y_0 )
			( = z z_0 )
			( = x_0 y_0 )
			( = y_0 0 )
			( = z_0 0 )
		)
	)
)

( define-fun trans-f ( ( x Int )( y Int )( z Int )( tmp Int )( x! Int )( y! Int )( z! Int )( tmp! Int )( x_0 Int )( y_0 Int )( z_0 Int )( z_1 Int ) ) Bool
	( or
		( and
			( = x x! )
			( = y y! )
			( = z z! )
			(= tmp tmp! )
		)
		( and
			(= x x_0 )
			(= x! x_0 )
			(= y y_0 )
			(= y! y_0 )
			(= z z_0 )
			(= z! z_0 )
			(= tmp tmp! )
		)
	)
)

( define-fun post-f ( ( x Int )( y Int )( z Int )( tmp Int )( x_0 Int )( y_0 Int )( z_0 Int )( z_1 Int ) ) Bool
	( and
		( or
			( not
				( and
					( = x x_0)
					( = y y_0)
					( = z z_0)
				)
			)
			( not
				( and
					( = x_0 y_0 )
					( >= x_0 0 )
					( not ( and ( and ( = x_0 y_0 ) ( >= x_0 0 ) ) ( = ( + ( + x_0 y_0 ) z_0 ) 0 ) ) )
				)
			)
		)
		( or
			( not
				( and
					( = x x_0)
					( = y y_0)
					( = z z_0)
				)
			)
			( not
				( and
					( = x_0 y_0 )
					( not ( >= x_0 0 ) )
					( not ( and ( and ( = x_0 y_0 ) ( >= x_0 0 ) ) ( = ( + ( + x_0 y_0 ) z_0 ) 0 ) ) )
				)
			)
		)
		( or
			( not
				( and
					( = x x_0)
					( = y y_0)
					( = z z_0)
				)
			)
			( not
				( and
					( not ( = x_0 y_0 ) )
					( not ( and ( and ( = x_0 y_0 ) ( >= x_0 0 ) ) ( = ( + ( + x_0 y_0 ) z_0 ) 0 ) ) )
				)
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f x y z tmp x_0 y_0 z_0 z_1  )
		( inv-f x y z tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f x y z tmp )
			( trans-f x y z tmp x! y! z! tmp! x_0 y_0 z_0 z_1 )
		)
		( inv-f x! y! z! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f x y z tmp  )
		( post-f x y z tmp x_0 y_0 z_0 z_1 )
	)
))

