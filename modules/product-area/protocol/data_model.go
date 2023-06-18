/* For license and copyright information please see the LEGAL file in the code repository */

package pap

import (
	"libgo/protocol"

	ep "org/modules/estate/protocol"
	prp "org/modules/product/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel is proper or appropriate location indicate specific area not specific location e.g. Taxi, ...
type DataModel interface {
	ProductID() prp.ProductUUID //
	EstateID() ep.EstateUUID    //
	Status() Status
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
