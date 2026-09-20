/* For license and copyright information please see the LEGAL file in the code repository */

package pmup

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
	product_p "org/modules/economics/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	product_p.Field_ProductID
	Maximum() uint64 // Maximum time this service can be served to buyer

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
