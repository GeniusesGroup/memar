/* For license and copyright information please see the LEGAL file in the code repository */

package brbp


type Type uint8

const (
	Type_Unset Type = iota
	Type_Blocking
	Type_Complement
	Type_Continuous
)
