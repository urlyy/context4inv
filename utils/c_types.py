"""Type tags used by the scalar and one-dimensional array abstraction."""

VAR_ARRAY = "array"
VAR_POINTER = "pointer"

# Scalars use (name,); arrays/pointers use (kind, (element_name,)).
type CType = tuple[str] | tuple[str, tuple[str]]
