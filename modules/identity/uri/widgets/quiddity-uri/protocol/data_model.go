/* For license and copyright information please see the LEGAL file in the code repository */

package qu_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	thing_p "org/modules/identity/thing/protocol"
)

// DataModel indicate the domain record data fields.
// https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
// https://en.wikipedia.org/wiki/Uniform_Resource_Name
// https://en.wikipedia.org/wiki/Electronic_Product_Code
type DataModel interface {
	Field_URI
	thing_p.Field_ThingUUID

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
