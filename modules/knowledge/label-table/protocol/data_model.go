/* For license and copyright information please see the LEGAL file in the code repository */

package lt_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"

	label_p "org/modules/knowledge/label/protocol"
)

// LabelTable indicate the domain record data fields.
// Table or boards is visual aid to help users access tasks in GUI e.g.Table(TODO, DOING, DONE)
// TODO::: base on label or status or both??
type LabelTable interface {
	Field_TableID
	label_p.Field_LabelsID

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
