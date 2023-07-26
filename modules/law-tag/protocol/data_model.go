/* For license and copyright information please see the LEGAL file in the code repository */

package ltp

import (
	"memar/protocol"

	lp "org/modules/law/protocol"
)

// DataModel or law hashtag indicate the domain record data fields.
type DataModel interface {
	LawID() lp.LawUUID
	Tag() string
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
