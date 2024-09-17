/* For license and copyright information please see the LEGAL file in the code repository */

package dpp

type Type uint16

const (
	Type_Unset     Type = 0           //
	Type_Mandatory Type = (1 << iota) // != optional
	Type_Pair                         //
)
