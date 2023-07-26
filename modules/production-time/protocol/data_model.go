/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	pp "org/modules/production/protocol"
)

// DataModel
type DataModel interface {
	ProductionID() pp.ProductionUUID
	TimeType() TimeType
	ActionTime() protocol.Time

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
