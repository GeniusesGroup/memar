/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// QuiddityModel indicate the domain record data fields.
// Model is the 3D model of the quiddity
type QuiddityModel interface {
	QuiddityID() [16]byte       // quiddity domain
	ObjectID() [32]byte         // object domain. ThingModel
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

// ProductAttribute_Type_MetricUnit // Number, Gram, Liter, Second
