/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	request_p "memar/audit/request/protocol"

	thing_p "org/modules/identity/thing/protocol"
	estate_p "org/modules/rights/estate/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	thing_p.Field_ThingID
	estate_p.Field_EstateID
	X() uint64 // Three-Dimensional Coordinate Systems
	Y() uint64 // Three-Dimensional Coordinate Systems
	Z() uint64 // Three-Dimensional Coordinate Systems

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
