/* For license and copyright information please see the LEGAL file in the code repository */

package qdp

import (
	"libgo/protocol"

	qp "org/modules/questionnaire/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() qp.QuestionnaireUUID //
	Epoch() QuestionnaireDuration_Epoch    //
	Duration() protocol.Duration           // from Epoch()
	SaveTime() protocol.Time               //
	RequestID() urp.UserRequestUUID        //
}

type QuestionnaireDuration_Epoch uint8

const (
	QuestionnaireDuration_Epoch_Unset QuestionnaireDuration_Epoch = iota
	QuestionnaireDuration_Epoch_IssueDate
	QuestionnaireDuration_Epoch_StartPoint
)
