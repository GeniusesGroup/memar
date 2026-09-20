/* For license and copyright information please see the LEGAL file in the code repository */

package ptip

import (
	"memar/time/duration"

	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
	product_p "org/modules/economics/product/protocol"
)

// DataModel indicate the domain record data fields.
// e.g. flight duration, doctor visit, carwash, ...
type DataModel interface {
	product_p.Field_ProductID
	Minimum() duration.Second  // Minimum time duration for this service
	Expected() duration.Second // Expected time duration for this service
	Maximum() duration.Second  // Maximum time duration for this service

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
