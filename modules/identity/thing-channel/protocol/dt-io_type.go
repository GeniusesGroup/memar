/* For license and copyright information please see the LEGAL file in the code repository */

package channel_p

type Field_IOType interface {
	// Type is for thing channel itself(receiver)
	// We know sender(usually related module for the thing like driver) has opposite type.
	Type() IOType
}

type IOType uint8

// Common flags
const (
	Type_Unset IOType = iota
	Type_Input
	Type_Output
)
