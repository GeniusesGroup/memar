/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/content/protocol"
)

type DataModel interface {
	ContentID() cp.ContentUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
