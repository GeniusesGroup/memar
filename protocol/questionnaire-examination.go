/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	
	urp "org/modules/user-request/protocol"
)

type QuestionnaireExaminationUUID protocol.UUID

// QuestionnaireExamination indicate the domain record data fields.
type QuestionnaireExamination interface {
	QuestionnaireExaminationID() QuestionnaireExaminationUUID //
	QuestionnaireOrderID() QuestionnaireOrderUUID             //
	AnswerBy() protocol.UserID                                //
	FillBy() protocol.UserID                                  //
	Time() protocol.Time                                      // Save time
	RequestID() urp.UserRequestUUID                           // user-request domain
}
