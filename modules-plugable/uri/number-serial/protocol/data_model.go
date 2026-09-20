/* For license and copyright information please see the LEGAL file in the code repository */

package irlp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
	inventory_p "org/modules/economics/inventory/protocol"
)

// DataModel indicate the domain record data fields.
// ProductInventory or good stock
type DataModel interface {
	inventory_p.Field_InventoryID
	SerialID_Start() string
	SerialID_End() string

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
