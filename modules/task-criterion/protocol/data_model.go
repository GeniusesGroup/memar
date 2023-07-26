/* For license and copyright information please see the LEGAL file in the code repository */

package tcp

import (
	"memar/protocol"

	tp "org/modules/task/protocol"
)

// DataModel indicate the domain record data fields.
// a basis for comparison; a reference point against which other things can be evaluated
// the ideal in terms of which something can be judged
type DataModel interface {
	TaskID() tp.TaskUUID
	Type() Type
	Point() Point

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
