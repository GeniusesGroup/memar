/* For license and copyright information please see the LEGAL file in the code repository */

package ggrrrp

import (
	"memar/protocol"
	ggp "org/modules/geography/protocol"
	ggrrl "org/modules/geography-region-relation-label/protocol"
)

type DataModel interface {
	RegionID() ggp.GeographyRegionUUID
	RelatedRegionID() ggp.GeographyRegionUUID
	RelationType() ggrrl.label

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
