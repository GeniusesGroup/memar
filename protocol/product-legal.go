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
	Save(dm ProductLegal) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, orgID OrgUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, orgID OrgUUID, vo protocol.VersionOffset) (dm ProductLegal, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_OrgID(orgID OrgUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_OrgIDs_By_ProductID(productID ProductUUID, offset, limit uint64) (orgIDs []OrgUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type Product_Legal_Type uint8

const (
	Product_Legal_Type_Unset Product_Legal_Type = iota
	Product_Legal_Type_Owner
	Product_Legal_Type_SettlementReference
	Product_Legal_Type_Supplier
	Product_Legal_Type_Distributer
)


// 	LIST_ProductIDs_BY_OrgID_AND_Type(orgID OrgUUID, t Product_Legal_Type, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
