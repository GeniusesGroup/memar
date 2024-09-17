/* For license and copyright information please see the LEGAL file in the code repository */

package qrqp

type Type uint8

const (
	Type_Unset Type = iota
	Type_SubQuestion
	Type_Translated
	Type_Complement
	Type_Hint // use for options not descriptive type.
)
