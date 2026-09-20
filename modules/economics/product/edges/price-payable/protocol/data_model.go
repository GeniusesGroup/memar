/* For license and copyright information please see the LEGAL file in the code repository */

package pppp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
	product_p "org/modules/economics/product/protocol"

	fmp "org/modules/economics/money/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel store historically price with discount to show to users in price change chart.
type DataModel interface {
	product_p.Field_ProductID
	// org_p.Field_OrganizationID
	Currency() uint64
	Price() fmp.Amount // Basic Price not payable price in the society currency

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
