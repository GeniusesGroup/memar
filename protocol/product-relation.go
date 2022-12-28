/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductRelation indicate the domain record data fields.
type ProductRelation interface {
	ProductID() ProductUUID                 //
	RelationID() ProductUUID                //
	RelationType() QuiddityRelationTypeUUID // رویه پیتزا؟؟    Optional??
	Quantity() uint64                       // decimal >> 1.5 >> 1.2 >> 10 >> 0
	Status() ProductRelation_Status         //
	Time() protocol.Time                    // save time
	RequestID() UserRequestUUID             // user-request domain
}

type ProductRelation_StorageServices interface {
	Save(pr ProductRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pr ProductRelation, nv protocol.NumberOfVersion, err protocol.Error)

	FindByRelation(RelationID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductRelation_Status uint8

const (
	ProductRelation_Status_Unset    ProductRelation_Status = 0
	ProductRelation_Status_Optional ProductRelation_Status = (1 << iota)
)
