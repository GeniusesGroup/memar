/* For license and copyright information please see the LEGAL file in the code repository */

package qrcp

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID    //
	Colors() []protocol.RGB         //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
