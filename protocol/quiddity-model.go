/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuiddityModel indicate the domain record data fields.
// Model is the 3D model of the quiddity
type QuiddityModel interface {
	QuiddityID() QuiddityUUID       //
	ObjectID() ObjectUUID           // ThingModel
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

// ProductAttribute_Type_MetricUnit // Number, Gram, Liter, Second
