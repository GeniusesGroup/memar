/* For license and copyright information please see the LEGAL file in the code repository */

package ttp

type Type uint8

const (
	Type_Unset Type = iota
	Type_ManualStart
	Type_ManualTemporaryEnd
	Type_ManualEnd
	Type_Start
	Type_TemporaryEnd
	Type_End
)
