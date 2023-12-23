/* For license and copyright information please see the LEGAL file in the code repository */

package ggrrup

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	grp "org/modules/geography-region/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	GeographyID() grp.GeographyRegionUUID
	UserID() up.UserUUID
	RelationType() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
