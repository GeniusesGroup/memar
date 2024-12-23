/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"
	pm_p "org/modules/business/product-material/protocol"
	prp "org/modules/business/production/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductionID() prp.UUID
	pm_p.DataModel

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
