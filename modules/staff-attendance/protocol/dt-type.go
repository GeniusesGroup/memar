/* For license and copyright information please see the LEGAL file in the code repository */

package sap

type Type uint8

const (
	Type_Unset Type = iota
	Type_Enter
	Type_Exit
	Type_ManualEnter
	Type_ManualExit
	Type_Start
	Type_End
)
