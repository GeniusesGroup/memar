/* For license and copyright information please see the LEGAL file in the code repository */

package tax_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	government_p "org/bundles/government/protocol"
)

// TODO::: change tax to a product instead of standalone model
// TODO::: change to `tax-payable-...`

// DataModel indicate the domain record data fields.
type DataModel interface {
	Field_TaxID
	government_p.Field_GovernmentID

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
