/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuiddityRelation indicate the domain record data fields.
// QuiddityRelation store some key/value for a Quiddity to describe it e.g. mobile-cpu, ...
// TODO::: is it good idea to add detail manually by users?? or quiddity-model is better??
type QuiddityRelation interface {
	QuiddityID() QuiddityUUID                //
	RelationID() QuiddityUUID                //
	RelationType() QuiddityRelationTypeUUID  // رویه پیتزا؟؟    Optional??
	RelationValue() QuiddityRelationTypeUUID // gram, liter, ...
	RelationDescription() QuiddityUUID       // TODO::: ??? 10gr?
	Status() QuiddityRelation_Status         //
	Time() protocol.Time                     // save time
	RequestID() urp.UserRequestUUID          //
}

type QuiddityRelation_StorageServices interface {
	Save(qr QuiddityRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID QuiddityUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID QuiddityUUID, vo protocol.VersionOffset) (qr QuiddityRelation, nv protocol.NumberOfVersion, err protocol.Error)

	FindByRelation(RelationID QuiddityUUID, offset, limit uint64) (quiddityIDs []QuiddityUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuiddityRelation_Status uint8
