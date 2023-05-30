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
	Save(pr ProductRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (pr ProductRelation, nv protocol.NumberOfVersion, err protocol.Error)

	FindByRelation(relationID ProductUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductRelation_Status uint8

const (
	ProductRelation_Status_Unset    ProductRelation_Status = 0
	ProductRelation_Status_Optional ProductRelation_Status = (1 << iota)
)

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
