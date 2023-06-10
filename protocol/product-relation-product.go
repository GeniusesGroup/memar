/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductRelation indicate the domain record data fields.
type ProductRelation interface {
	ProductID() ProductUUID                 //
	RelationID() ProductUUID                //
	RelationType() QuiddityRelationTypeUUID // رویه پیتزا؟؟    Optional??
	Quantity() uint64                       // decimal >> 1.5 >> 1.2 >> 10 >> 0
	MaxQuantity() uint64                    //
	Status() ProductRelation_Status         //
	Time() protocol.Time                    // save time
	RequestID() urp.UserRequestUUID         //
}

type ProductRelation_StorageServices interface {
	Save(dm ProductRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, relationID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, relationID ProductUUID, vo protocol.VersionOffset) (dm ProductRelation, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_RelationID(relationID ProductUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RelationIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (relationIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductRelation_Status Quiddity_Status

const (
	ProductRelation_Status_Optional = ProductRelation_Status(Quiddity_Status_FreeFlag << iota)
)

// 	FIND_ProductIDs_BY_RelationID_AND_Type(relationID ProductUUID, t QuiddityRelationTypeUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)

type mealDeal struct {
	products []struct {
		productID string
		maxNum    int
	}
	categories []struct {
		categoryID string
		maxNum     int
	}
}
