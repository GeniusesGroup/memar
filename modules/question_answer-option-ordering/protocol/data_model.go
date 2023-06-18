/* For license and copyright information please see the LEGAL file in the code repository */

package qaoop

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID            //
	OptionsOrder() []qop.QuestionOptionUUID //
	SaveTime() protocol.Time                // Save time
	RequestID() urp.UserRequestUUID         //
}

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID qp.QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID qp.QuestionUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
