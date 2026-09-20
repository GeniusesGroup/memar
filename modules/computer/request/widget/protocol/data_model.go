/* For license and copyright information please see the LEGAL file in the code repository */

package rrr_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	label_p "org/modules/knowledge/label/protocol"
	graph_p "org/modules/storage/graph/protocol"
)

// DataModel indicates the domain record data fields.
type DataModel interface {
	graph_p.DataModel[request_p.UUID, request_p.UUID, label_p.UUID]

	// With this number we can show user how many changes
	// ChainNumber() container_p.NumberOfElement

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
