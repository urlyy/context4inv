(set-logic LIA)

( declare-const w Int )
( declare-const w! Int )
( declare-const x Int )
( declare-const x! Int )
( declare-const y Int )
( declare-const y! Int )
( declare-const z Int )
( declare-const z! Int )
( declare-const tmp Int )
( declare-const tmp! Int )

( declare-const w_0 Int )
( declare-const x_0 Int )
( declare-const y_0 Int )
( declare-const z_0 Int )

( define-fun inv-f( ( w Int )( x Int )( y Int )( z Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( w Int )( x Int )( y Int )( z Int )( tmp Int )( w_0 Int )( x_0 Int )( y_0 Int )( z_0 Int ) ) Bool
	( and
		( = w w_0 )
		( = x x_0 )
		( = y y_0 )
		( = z z_0 )
		( = x_0 w_0 )
		( = y_0 ( + w_0 1 ) )
		( = z_0 ( + x_0 1 ) )
	)
)

( define-fun trans-f ( ( w Int )( x Int )( y Int )( z Int )( tmp Int )( w! Int )( x! Int )( y! Int )( z! Int )( tmp! Int )( w_0 Int )( x_0 Int )( y_0 Int )( z_0 Int ) ) Bool
	( or
		( and
			( = w w! )
			( = x x! )
			( = y y! )
			( = z z! )
			(= tmp tmp! )
		)
		( and
			(= w w_0 )
			(= w! w_0 )
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

( define-fun post-f ( ( w Int )( x Int )( y Int )( z Int )( tmp Int )( w_0 Int )( x_0 Int )( y_0 Int )( z_0 Int ) ) Bool
	( or
		( not
			( and
				( = w w_0)
				( = x x_0)
				( = y y_0)
				( = z z_0)
			)
		)
		( not
			( and
				( not ( = y_0 z_0 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f w x y z tmp w_0 x_0 y_0 z_0  )
		( inv-f w x y z tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f w x y z tmp )
			( trans-f w x y z tmp w! x! y! z! tmp! w_0 x_0 y_0 z_0 )
		)
		( inv-f w! x! y! z! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f w x y z tmp  )
		( post-f w x y z tmp w_0 x_0 y_0 z_0 )
	)
))

