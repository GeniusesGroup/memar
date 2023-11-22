/* For license and copyright information please see the LEGAL file in the code repository */

package ap

import (
	"memar/protocol"
)

type DataModel interface {
	AppID() AppUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
