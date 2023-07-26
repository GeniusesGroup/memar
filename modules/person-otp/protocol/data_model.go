/* For license and copyright information please see the LEGAL file in the code repository */

package pop

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	PersonID() up.UserUUID
	OTPPattern() []byte   // https://tools.ietf.org/html/rfc6238
	OTPAdditional() int32 // easy to remember and must be 2 to 7 digit. https://en.wikipedia.org/wiki/Personal_identification_number

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
