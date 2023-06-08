/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type QuestionnaireRespondentUUID protocol.UUID

// QuestionnaireRespondent indicate the domain record data fields.
type QuestionnaireRespondent interface {
	QuestionnaireRespondentID() QuestionnaireRespondentUUID //
	QuestionnaireOrderID() QuestionnaireOrderUUID           //
	AnswerBy() up.UserUUID                                  //
	FillBy() up.UserUUID                                    //
	Time() protocol.Time                                    // Save time
	RequestID() urp.UserRequestUUID                         //
}

type QuestionnaireRespondent_StorageServices interface {
	Save(dm QuestionnaireRespondent) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireRespondentID QuestionnaireRespondentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireRespondentID QuestionnaireRespondentUUID, vo protocol.VersionOffset) (dm QuestionnaireRespondent, nv protocol.NumberOfVersion, err protocol.Error)
}
