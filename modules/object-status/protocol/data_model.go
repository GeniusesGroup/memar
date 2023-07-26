/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	"memar/protocol"

	op "org/modules/object/protocol"
)

type DataModel interface {
	ObjectID() op.ObjectUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
