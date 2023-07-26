/* For license and copyright information please see the LEGAL file in the code repository */

package bmap

type Type uint8

const (
	Type_Unset Type = iota
	Type_Suggested
	Type_Approved
	Type_Executed
	Type_Inspected
)
