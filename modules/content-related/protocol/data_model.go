/* For license and copyright information please see the LEGAL file in the code repository */

package crp

import (
	"memar/protocol"

	ctp "org/modules/content-type/protocol"
	cp "org/modules/content/protocol"
)

type DataModel interface {
	ContentID() cp.ContentUUID
	Priority() uint64
	PriorityType() ctp.ContentTypeUUID
	RelatedID() cp.ContentUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
