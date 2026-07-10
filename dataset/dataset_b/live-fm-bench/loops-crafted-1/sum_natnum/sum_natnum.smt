(set-logic LIA)

( declare-const SIZE Int )
( declare-const SIZE! Int )
( declare-const i Int )
( declare-const i! Int )
( declare-const sum Int )
( declare-const sum! Int )

( declare-const SIZE_0 Int )
( declare-const i_0 Int )
( declare-const i_1 Int )
( declare-const i_2 Int )
( declare-const i_3 Int )
( declare-const sum_0 Int )
( declare-const sum_1 Int )
( declare-const sum_2 Int )
( declare-const sum_3 Int )

( define-fun inv-f( ( SIZE Int )( i Int )( sum Int ) ) Bool
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
)

( define-fun pre-f ( ( SIZE Int )( i Int )( sum Int )( SIZE_0 Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int )( sum_0 Int )( sum_1 Int )( sum_2 Int )( sum_3 Int ) ) Bool
	( and
		( = SIZE SIZE_0 )
		( = i i_1 )
		( = sum sum_1 )
		( = SIZE_0 40000 )
		( = i_1 0 )
		( = sum_1 0 )
	)
)

( define-fun trans-f ( ( SIZE Int )( i Int )( sum Int )( SIZE! Int )( i! Int )( sum! Int )( SIZE_0 Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int )( sum_0 Int )( sum_1 Int )( sum_2 Int )( sum_3 Int ) ) Bool
	( or
		( and
			( = i_2 i )
			( = sum_2 sum )
			( = i_2 i! )
			( = sum_2 sum! )
			( = SIZE SIZE_0 )
			( = SIZE! SIZE_0 )
			( = sum sum! )
		)
		( and
			( = i_2 i )
			( = sum_2 sum )
			( < i_2 SIZE_0 )
			( = i_3 ( + i_2 1 ) )
			( = sum_3 ( + sum_2 i_3 ) )
			( = i_3 i! )
			( = sum_3 sum! )
			(= SIZE SIZE_0 )
			(= SIZE! SIZE_0 )
		)
	)
)

( define-fun post-f ( ( SIZE Int )( i Int )( sum Int )( SIZE_0 Int )( i_0 Int )( i_1 Int )( i_2 Int )( i_3 Int )( sum_0 Int )( sum_1 Int )( sum_2 Int )( sum_3 Int ) ) Bool
	( or
		( not
			( and
				( = SIZE SIZE_0)
				( = i i_2)
				( = sum sum_2)
			)
		)
		( not
			( and
				( not ( < i_2 SIZE_0 ) )
				( not ( = sum_2 ( / ( * SIZE_0 ( + SIZE_0 1 ) ) 2 ) ) )
			)
		)
	)
)
SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( pre-f SIZE i sum SIZE_0 i_0 i_1 i_2 i_3 sum_0 sum_1 sum_2 sum_3  )
		( inv-f SIZE i sum )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( and
			( inv-f SIZE i sum )
			( trans-f SIZE i sum SIZE! i! sum! SIZE_0 i_0 i_1 i_2 i_3 sum_0 sum_1 sum_2 sum_3 )
		)
		( inv-f SIZE! i! sum! )
	)
))

SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop
( assert ( not
	( =>
		( inv-f SIZE i sum  )
		( post-f SIZE i sum SIZE_0 i_0 i_1 i_2 i_3 sum_0 sum_1 sum_2 sum_3 )
	)
))

