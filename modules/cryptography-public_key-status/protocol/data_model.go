/* For license and copyright information please see the LEGAL file in the code repository */

package cpksp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cpkp "org/modules/cryptography-public_key/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	PublicKeyID() cpkp.PublicKeyUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
