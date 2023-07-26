/* For license and copyright information please see the LEGAL file in the code repository */

package prp

type Type uint8

const (
	Type_Unset     Type = iota
	Type_SellLimit      // limit sell to specific roles.
	Type_Approver
	// Type_
)
