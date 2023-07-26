/* For license and copyright information please see the LEGAL file in the code repository */

package qmsp

import (
	"memar/protocol"

	op "org/modules/object/protocol"
	qp "org/modules/quiddity/protocol"
)

type DataModel interface {
	QuiddityID() qp.QuiddityUUID
	MediaObjectID() op.ObjectUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
