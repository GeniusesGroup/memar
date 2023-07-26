/* For license and copyright information please see the LEGAL file in the code repository */

package dop

import (
	"memar/protocol"

	dp "org/modules/discount/protocol"
	org "org/modules/org/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID
	OrgID() org.OrgUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
