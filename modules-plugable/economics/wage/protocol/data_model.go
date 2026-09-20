/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	oidp "org/modules/economics/order-item-deal/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	OrderKind() oidp.Order_Kind
	PerMyriad()
	Amount()

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
