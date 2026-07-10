(set-logic LIA)

( declare-const i Int )
( declare-const i! Int )
( declare-const j Int )
( declare-const j! Int )
( declare-const k Int )
( declare-const k! Int )
( declare-const x Int )
( declare-const x! Int )
( declare-const y Int )
( declare-const y! Int )
( declare-const tmp Int )
( declare-const tmp! Int )

( declare-const i_0 Int )
( declare-const j_0 Int )
( declare-const j_1 Int )
( declare-const k_0 Int )
( declare-const x_0 Int )
( declare-const y_0 Int )

( define-fun inv-f( ( i Int )( j Int )( k Int )( x Int )( y Int )( tmp Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( i Int )( j Int )( k Int )( x Int )( y Int )( tmp Int )( i_0 Int )( j_0 Int )( j_1 Int )( k_0 Int )( x_0 Int )( y_0 Int ) ) Bool
	( or
		( and
			( = j j_1 )
			( = k k_0 )
			( = x x_0 )
			( = y y_0 )
			( = j_1 0 )
			( = ( + x_0 y_0 ) k_0 )
		)
	)
)

( define-fun trans-f ( ( i Int )( j Int )( k Int )( x Int )( y Int )( tmp Int )( i! Int )( j! Int )( k! Int )( x! Int )( y! Int )( tmp! Int )( i_0 Int )( j_0 Int )( j_1 Int )( k_0 Int )( x_0 Int )( y_0 Int ) ) Bool
	( or
		( and
			( = i i! )
			( = j j! )
			( = k k! )
			( = x x! )
			( = y y! )
			(= tmp tmp! )
		)
		( and
			( = j_1 i_0 )
			(= i i_0 )
			(= i! i_0 )
			(= j j_1 )
			(= j! j_1 )
			(= k k_0 )
			(= k! k_0 )
			(= x x_0 )
			(= x! x_0 )
			(= y y_0 )
			(= y! y_0 )
			(= tmp tmp! )
		)
		( and
			( not ( = j_1 i_0 ) )
			(= i i_0 )
			(= i! i_0 )
			(= j j_1 )
			(= j! j_1 )
			(= k k_0 )
			(= k! k_0 )
			(= x x_0 )
			(= x! x_0 )
			(= y y_0 )
			(= y! y_0 )
			(= tmp tmp! )
		)
	)
)

( define-fun post-f ( ( i Int )( j Int )( k Int )( x Int )( y Int )( tmp Int )( i_0 Int )( j_0 Int )( j_1 Int )( k_0 Int )( x_0 Int )( y_0 Int ) ) Bool
	( or
		( not
			( and
				( = i i_0 )
				( = j j_1)
				( = k k_0)
				( = x x_0)
				( = y y_0)
			)
		)
		( not
			( and
				( not ( = ( + x_0 y_0 ) k_0 ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f i j k x y tmp i_0 j_0 j_1 k_0 x_0 y_0  )
		( inv-f i j k x y tmp )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f i j k x y tmp )
			( trans-f i j k x y tmp i! j! k! x! y! tmp! i_0 j_0 j_1 k_0 x_0 y_0 )
		)
		( inv-f i! j! k! x! y! tmp! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f i j k x y tmp  )
		( post-f i j k x y tmp i_0 j_0 j_1 k_0 x_0 y_0 )
	)
))

