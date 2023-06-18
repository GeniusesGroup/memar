/* For license and copyright information please see the LEGAL file in the code repository */

package qrp

import (
	"libgo/protocol"

	qrtp "org/modules/quiddity-relation-type/protocol"
	qp "org/modules/quiddity/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel store some key/value for a Quiddity to describe it e.g. mobile-cpu, ...
// TODO::: is it good idea to add detail manually by users?? or quiddity-model is better??
type DataModel interface {
	QuiddityID() qp.QuiddityUUID                  //
	RelationID() qp.QuiddityUUID                  //
	RelationType() qrtp.QuiddityRelationTypeUUID  // رویه پیتزا؟؟    Optional??
	RelationValue() qrtp.QuiddityRelationTypeUUID // gram, liter, ...
	RelationDescription() qp.QuiddityUUID         // TODO::: ??? 10gr?
	Status() Status                               //
	SaveTime() protocol.Time                      //
	RequestID() urp.UserRequestUUID               //
}

type Status uint8
