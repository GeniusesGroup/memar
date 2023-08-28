/* For license and copyright information please see the LEGAL file in the code repository */

package itp

import (
	"memar/protocol"

	ip "org/modules/inventory/protocol"
)

// Some resource:
// https://www.odoo.com/documentation/16.0/applications/inventory_and_mrp/inventory/management/lots_serial_numbers/lots.html

// DataModel indicate the domain record data fields.
type DataModel interface {
	InventoryID() ip.InventoryUUID
	ReferenceType() ReferenceType
	ReferenceID() protocol.UUID // Depend on ReferenceType()
	Amount() int64              // this transaction
	Stock() int64               // overall in each location

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
