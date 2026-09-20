/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionQuestionRelation indicate the domain record data fields.
type QuestionQuestionRelation_StorageFields interface {
	QuestionID() QuestionUUID                //
	RelationID() QuestionUUID                //
	Type() QuestionQuestionRelation_Type     //
	Status() QuestionQuestionRelation_Status //
	Time() protocol.Time                     // Save time
	RequestID() urp.UserRequestUUID          //
}

type QuestionQuestionRelation_StorageIndexes interface {
	ClusterKey()
	PrimaryKey() (questionID QuestionUUID)
	SecondaryIndex_1() (questionID QuestionUUID)
}

type QuestionQuestionRelation_StorageServices interface {
	Search_RelationID_Type(relationID QuestionUUID, t QuestionQuestionRelation_Type, offset, limit uint64) (questionID []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByType(t QuestionQuestionRelation_Type, offset, limit uint64) (questionID []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)

	ListAllQuestionRelations(questionID QuestionUUID, offset, limit uint64) (relationID []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
	
	FindUser
}

type addressbook_Person_Request interface {
	name() string
	id() int32
	email() string
	PhoneNumber() []struct {
		number    string
		PhoneType Phone_Type
	}
	last_updated() google.protobuf.Timestamp
}

type Phone_Type uint8

const (
	Phone_Type_MOBILE = 0
	Phone_Type_HOME   = 1
	Phone_Type_WORK   = 2
)

type QuestionQuestionRelation_Type uint8

const (
	QuestionQuestionRelation_Type_Unset QuestionQuestionRelation_Type = iota
	QuestionQuestionRelation_Type_SubQuestion
	QuestionQuestionRelation_Type_Translated
	QuestionQuestionRelation_Type_Complement
	QuestionQuestionRelation_Type_Hint // use for options not descriptive type.
)

type QuestionQuestionRelation_Status Quiddity_Status
