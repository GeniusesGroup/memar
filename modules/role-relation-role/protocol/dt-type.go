/* For license and copyright information please see the LEGAL file in the code repository */

package rrrp

type Type uint8

const (
	Type_Unset Type = iota
	Type_SameLevel
	Type_UpperLevel
	Type_LowerLevel
)
