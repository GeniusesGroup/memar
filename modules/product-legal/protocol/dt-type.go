/* For license and copyright information please see the LEGAL file in the code repository */

package plp

type Type uint8

const (
	Type_Unset Type = iota
	Type_Owner
	Type_SettlementReference
	Type_Supplier
	Type_Distributer
)
