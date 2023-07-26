/* For license and copyright information please see the LEGAL file in the code repository */

package trlp

import (
	"memar/protocol"

	lp "org/modules/label/protocol"
	tp "org/modules/task/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID
	Label() lp.LabelUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// default labels:
// 	Type_Compliment
// 	Type_Suggestion
// 	Type_Issue
