/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	
	urp "org/modules/user-request/protocol"
)

// QuestionnaireDuration indicate the domain record data fields.
type QuestionnaireDuration interface {
	QuestionnaireID() QuestionnaireUUID //
	Epoch() QuestionnaireDuration_Epoch //
	Duration() protocol.Duration        // from Epoch()
	Time() protocol.Time                // save time
	RequestID() urp.UserRequestUUID     // user-request domain
}

type QuestionnaireDuration_Epoch uint8

const (
	QuestionnaireDuration_Epoch_Unset QuestionnaireDuration_Epoch = iota
	QuestionnaireDuration_Epoch_IssueDate
	QuestionnaireDuration_Epoch_StartPoint
)
