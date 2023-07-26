/* For license and copyright information please see the LEGAL file in the code repository */

package cip

import (
	"memar/protocol"

	cp "org/modules/category/protocol"
)

type DataModel interface {
	CategoryID() cp.CategoryUUID
	Priority() uint64
	ItemID() protocol.UUID // any domain usually product, content, ... domain

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
