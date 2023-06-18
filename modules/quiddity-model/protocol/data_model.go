/* For license and copyright information please see the LEGAL file in the code repository */

package qmp

import (
	"libgo/protocol"

	op "org/modules/object/protocol"
	qp "org/modules/quiddity/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// Model is the 3D model of the quiddity
type DataModel interface {
	QuiddityID() qp.QuiddityUUID    //
	ObjectID() op.ObjectUUID        // ThingModel
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

// ProductAttribute_Type_MetricUnit // Number, Gram, Liter, Second
