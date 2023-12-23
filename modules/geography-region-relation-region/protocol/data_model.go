/* For license and copyright information please see the LEGAL file in the code repository */

package ggrrrp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	grp "org/modules/geography-region/protocol"
	lp "org/modules/label/protocol"
)

type DataModel interface {
	RegionID() grp.GeographyRegionUUID
	RelatedRegionID() grp.GeographyRegionUUID
	RelationType() lp.LabelUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
