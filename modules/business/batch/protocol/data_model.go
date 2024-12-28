/* For license and copyright information please see the LEGAL file in the code repository */

package batch_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"
	decimal_p "memar/math/decimal/protocol"

	product_p "org/modules/business/product/protocol"
)

// DataModel is the structure of production line.
type DataModel interface {
	Field_BatchID
	product_p.Field_ProductID
	decimal_p.Field_Quantity

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
