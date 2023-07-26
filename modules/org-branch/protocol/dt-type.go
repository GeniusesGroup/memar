/* For license and copyright information please see the LEGAL file in the code repository */

package obp

type Type uint8

const (
	Type_Unset Type = iota
	Type_Online
	Type_Branch
	Type_Agent
	Type_Franchise
)
