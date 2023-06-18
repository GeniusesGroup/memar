/* For license and copyright information please see the LEGAL file in the code repository */

package prpp

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
	qrtp "org/modules/quiddity-relation-type/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID                   //
	RelationID() pp.ProductUUID                  //
	RelationType() qrtp.QuiddityRelationTypeUUID // رویه پیتزا؟؟    Optional??
	Quantity() uint64                            // decimal >> 1.5 >> 1.2 >> 10 >> 0
	MaxQuantity() uint64                         //
	Status() Status                              //
	SaveTime() protocol.Time                     //
	RequestID() urp.UserRequestUUID              //
}

type Status qsp.Quiddity_Status

const (
	Status_Optional = Status(qsp.Quiddity_Status_FreeFlag << iota)
)
