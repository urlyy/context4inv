(set-logic LIA)

( declare-const high Int )
( declare-const high! Int )
( declare-const low Int )
( declare-const low! Int )
( declare-const mid Int )
( declare-const mid! Int )

( declare-const high_0 Int )
( declare-const high_1 Int )
( declare-const high_2 Int )
( declare-const high_3 Int )
( declare-const low_0 Int )
( declare-const low_1 Int )
( declare-const low_2 Int )
( declare-const low_3 Int )
( declare-const mid_0 Int )
( declare-const mid_1 Int )
( declare-const mid_2 Int )
( declare-const mid_3 Int )

( define-fun inv-f( ( high Int )( low Int )( mid Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( high Int )( low Int )( mid Int )( high_0 Int )( high_1 Int )( high_2 Int )( high_3 Int )( low_0 Int )( low_1 Int )( low_2 Int )( low_3 Int )( mid_0 Int )( mid_1 Int )( mid_2 Int )( mid_3 Int ) ) Bool
	( or
		( and
			( = high high_0 )
			( = low low_0 )
			( = mid mid_0 )
			( = low_0 0 )
			( >= mid_0 1 )
			( = high_0 ( * 2 mid_0 ) )
		)
	)
)

( define-fun trans-f ( ( high Int )( low Int )( mid Int )( high! Int )( low! Int )( mid! Int )( high_0 Int )( high_1 Int )( high_2 Int )( high_3 Int )( low_0 Int )( low_1 Int )( low_2 Int )( low_3 Int )( mid_0 Int )( mid_1 Int )( mid_2 Int )( mid_3 Int ) ) Bool
	( or
		( and
			( = high_1 high )
			( = low_1 low )
			( = mid_1 mid )
			( = high_1 high! )
			( = low_1 low! )
			( = mid_1 mid! )
			( = high high! )
			( = low low! )
		)
		( and
			( = high_1 high )
			( = low_1 low )
			( = mid_1 mid )
			( > mid_1 0 )
			( = low_2 ( + low_1 1 ) )
			( = high_2 ( - high_1 1 ) )
			( = mid_2 ( - mid_1 1 ) )
			( = high_2 high! )
			( = low_2 low! )
			( = mid_2 mid! )
		)
	)
)

( define-fun post-f ( ( high Int )( low Int )( mid Int )( high_0 Int )( high_1 Int )( high_2 Int )( high_3 Int )( low_0 Int )( low_1 Int )( low_2 Int )( low_3 Int )( mid_0 Int )( mid_1 Int )( mid_2 Int )( mid_3 Int ) ) Bool
	( or
		( not
			( and
				( = high high_1)
				( = low low_1)
				( = mid mid_1)
			)
		)
		( not
			( and
				( not ( > mid_1 0 ) )
				( not ( = low_1 high_1 ) )
				( = high_3 high_1 )
				( = low_3 low_1 )
				( = mid_3 mid_1 )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f high low mid high_0 high_1 high_2 high_3 low_0 low_1 low_2 low_3 mid_0 mid_1 mid_2 mid_3  )
		( inv-f high low mid )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f high low mid )
			( trans-f high low mid high! low! mid! high_0 high_1 high_2 high_3 low_0 low_1 low_2 low_3 mid_0 mid_1 mid_2 mid_3 )
		)
		( inv-f high! low! mid! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f high low mid  )
		( post-f high low mid high_0 high_1 high_2 high_3 low_0 low_1 low_2 low_3 mid_0 mid_1 mid_2 mid_3 )
	)
))

