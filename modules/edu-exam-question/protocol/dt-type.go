/* For license and copyright information please see the LEGAL file in the code repository */

package eeqp

type Type uint8

const (
	Type_Unset Type = iota
	Type_SingleChoice
	Type_MultipleChoice
	Type_Descriptive
)
