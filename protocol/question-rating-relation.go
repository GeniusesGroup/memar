/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionRating indicate the domain record data fields.
type QuestionRatingRelation interface {
	QuestionID() QuestionUUID                     //
	RelationIDs() [][16]byte                      // Question, Questionnaire
	RelationTypes() []QuestionRatingRelation_Type //
	Time() protocol.Time                          // Save time
	RequestID() urp.UserRequestUUID               // user-request domain
}

type QuestionRatingRelation_StorageServices interface {
	Save(f QuestionRatingRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (f QuestionRatingRelation, nv protocol.NumberOfVersion, err protocol.Error)

}

type QuestionRatingRelation_Type uint16

const (
	QuestionRatingRelation_Type_Question QuestionRatingRelation_Type = iota
	QuestionRatingRelation_Type_Questionnaire
)
