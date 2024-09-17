/* For license and copyright information please see the LEGAL file in the code repository */

package pp

type Type uint64

// Common flags
const (
	Type_Unset Type = 0
	Type_Cash  Type = (1 << iota)
	Type_Location
	Type_Provider
	Type_Product
	// Type_
)
