/* For license and copyright information please see the LEGAL file in the code repository */

package dlp

import (
	"memar/protocol"

	dp "org/modules/discount/protocol"
	bp "org/modules/estate-building-location/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID
	BuildingLocationID() bp.BuildingLocationUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
