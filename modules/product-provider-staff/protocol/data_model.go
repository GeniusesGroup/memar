/* For license and copyright information please see the LEGAL file in the code repository */

package ppsp

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
	sp "org/modules/staff/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	StaffID() sp.StaffUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
