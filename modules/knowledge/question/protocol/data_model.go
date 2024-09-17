/* For license and copyright information please see the LEGAL file in the code repository */

package qp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
)

// TODO::: dynamic data in question?? text substitution, text piping

// DataModel indicate the domain record data fields.
// DataModel text, videos, images, ... save in Comment domains.
type DataModel interface {
	QuestionID() QuestionUUID
	Type() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

type Question_GUI_Widget interface {
}
