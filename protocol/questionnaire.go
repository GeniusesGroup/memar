/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type QuestionnaireUUID protocol.UUID

// Questionnaire indicate the domain record data fields.
type Questionnaire interface {
	QuestionnaireID() QuestionnaireUUID //
	Type() Questionnaire_Type           //
	Time() protocol.Time                // Save time
	RequestID() urp.UserRequestUUID     //
}

type Questionnaire_StorageServices interface {
	Save(pc Questionnaire) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireID QuestionnaireUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireID QuestionnaireUUID, vo protocol.VersionOffset) (pc Questionnaire, nv protocol.NumberOfVersion, err protocol.Error)
}

type Questionnaire_Type uint16

const (
	Questionnaire_Type_Unset Questionnaire_Type = 0
	Questionnaire_Type_Quiz  Questionnaire_Type = (1 << iota)
	Questionnaire_Type_Anonymous
	Questionnaire_Type_Duration
	Questionnaire_Type_StartPoint
	Questionnaire_Type_AllowToEdit
	Questionnaire_Type_Form
	Questionnaire_Type_MaxAttempt

	// No one can made direct answer to this questionnaire.
	Questionnaire_Type_Criterion

	// TODO::: Template for forms?
)

// link to group
