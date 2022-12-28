/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// QuiddityRelation indicate the domain record data fields.
// QuiddityRelation store some key/value for a Quiddity to describe it e.g. mobile-cpu, ...
// TODO::: is it good idea to add detail manually by users?? or quiddity-model is better??
type QuiddityRelation interface {
	QuiddityID() QuiddityUUID                // product domain
	RelationID() QuiddityUUID                // product domain
	RelationType() QuiddityRelationTypeUUID  // رویه پیتزا؟؟    Optional??
	RelationValue() QuiddityRelationTypeUUID // gram, liter, ...
	RelationDescription() string             // TODO::: ??? 10gr?
	Status() QuiddityRelation_Status         //
	Time() protocol.Time                     // save time
	RequestID() UserRequestUUID              // user-request domain
}

type QuiddityRelation_StorageServices interface {
	Save(qr QuiddityRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (qr QuiddityRelation, nv protocol.NumberOfVersion, err protocol.Error)

	FindByRelation(RelationID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuiddityRelation_Status uint8
