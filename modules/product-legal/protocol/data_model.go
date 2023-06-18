/* For license and copyright information please see the LEGAL file in the code repository */

package plp

import (
	"libgo/protocol"

	org "org/modules/org/protocol"
	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID      //
	OrgID() org.OrgUUID             //
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_Owner
	Type_SettlementReference
	Type_Supplier
	Type_Distributer
)
