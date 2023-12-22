/* For license and copyright information please see the LEGAL file in the code repository */

package ggrrup

import (
	"memar/protocol"
	up "org/modules/user/protocol"
	ggrp "org/modules/geography-region/protocol"
)

type DataModel interface {
	GeographyID() ggrp.GeographyRegionUUID
	UserID() up.UserUUID
	RelationType() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
