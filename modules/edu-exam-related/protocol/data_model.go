/* For license and copyright information please see the LEGAL file in the code repository */

package eerp

import (
	"memar/protocol"

	exp "org/modules/edu-exam/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	SuggesterID() up.UserUUID
	Side1() exp.EducationExamUUID
	Priority() uint64
	Level() uint64
	Side2() exp.EducationExamUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
