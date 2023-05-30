/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductLegal indicate the domain record data fields.
type ProductLegal interface {
	ProductID() ProductUUID         //
	OrgID() OrgUUID                 //
	Type() Product_Legal_Type       //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductLegal_StorageServices interface {
	Save(po ProductLegal) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (po ProductLegal, nv protocol.NumberOfVersion, err protocol.Error)

	FindByOrg(orgID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type Product_Legal_Type uint8

const (
	Product_Legal_Type_Unset Product_Legal_Type = iota
	Product_Legal_Type_Owner
	Product_Legal_Type_SettlementReference
	Product_Legal_Type_Supplier
	Product_Legal_Type_Distributer
)
