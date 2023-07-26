/* For license and copyright information please see the LEGAL file in the code repository */

package qrp

import (
	"memar/protocol"

	qrtp "org/modules/quiddity-relation-type/protocol"
	qp "org/modules/quiddity/protocol"
)

// DataModel indicate the domain record data fields.
// QuiddityRelation store some key/value for a Quiddity to describe it e.g. mobile-cpu, ...
// TODO::: is it good idea to add detail manually by users?? or quiddity-model is better??
type DataModel interface {
	QuiddityID() qp.QuiddityUUID                  // mobile / Pizza
	RelationID() qp.QuiddityUUID                  // cpu / Cheese
	RelationType() qrtp.QuiddityRelationTypeUUID  // internal / رویه پیتزا؟؟    Optional??
	RelationValue() qrtp.QuiddityRelationTypeUUID // Hz, core / gram, liter, ...
	RelationDescription() qp.QuiddityUUID         // 2300, 4 / TODO::: ??? 10gr?
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
