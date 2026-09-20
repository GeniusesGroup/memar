/* For license and copyright information please see the LEGAL file in the code repository */

package nr_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	instance_p "org/modules/computer/instance_of/protocol"
	label_p "org/modules/knowledge/label/protocol"
)

type DataModel interface {
	instance_p.Field_InstanceUUID
	Type() label_p.UUID
	ResourceType() []ResourceType
	ResourceAmount() []string

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
