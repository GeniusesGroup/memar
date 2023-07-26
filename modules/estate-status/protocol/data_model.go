/* For license and copyright information please see the LEGAL file in the code repository */

package esp

import (
	"memar/protocol"

	ep "org/modules/estate/protocol"
)

type DataModel interface {
	EstateID() ep.EstateUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
