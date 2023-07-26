/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	pp "org/modules/production/protocol"
)

type DataModel interface {
	// A lot number is an identification number assigned to a particular quantity or lot of material from a single manufacturer.
	// https://en.wikipedia.org/wiki/Lot_number
	LOT() [16]byte
	ProductionID() pp.ProductionUUID
	StartDate() protocol.Time
	EndDate() protocol.Time
	Number() uint64
	Status() uint8

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
