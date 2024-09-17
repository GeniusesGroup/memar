/* For license and copyright information please see the LEGAL file in the code repository */

package ggrrop

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	grp "org/modules/geography-region/protocol"
	lp "org/modules/label/protocol"
)

type DataModel interface {
	GeographyRegionID() grp.GeographyRegionUUID
	LabelID() lp.LabelUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
