/* For license and copyright information please see the LEGAL file in the code repository */

package anlp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	instance_p "org/modules/computer/instance_of/protocol"
	language_p "org/modules/knowledge/language-human/protocol"
)

type DataModel interface {
	instance_p.Field_InstanceUUID
	language_p.Field_LanguageUUID
	Status()

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
