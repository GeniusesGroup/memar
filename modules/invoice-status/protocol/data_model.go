/* For license and copyright information please see the LEGAL file in the code repository */

package isp

import (
	"memar/protocol"

	ip "org/modules/invoice/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
