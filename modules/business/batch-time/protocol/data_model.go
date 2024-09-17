/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	pbp "org/modules/production-batch/protocol"
)

// DataModel is the structure of production line.
type DataModel interface {
	ProductionBatchID() pbp.ProductionBatchUUID
	TimeType() TimeType
	ActionTime() protocol.Time

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
