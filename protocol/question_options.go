/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionOptions indicate the domain record data fields.
type QuestionOptions interface {
	QuestionID() QuestionUUID                     //
	Options() []QuestionOptionUUID                //
	Type() QuestionOptions_Type                   //
	AlgorithmType() QuestionOptions_AlgorithmType //
	Time() protocol.Time                          // Save time
	RequestID() urp.UserRequestUUID               //
}

type QuestionOptions_StorageServices interface {
	Save(f QuestionOptions) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (f QuestionOptions, nv protocol.NumberOfVersion, err protocol.Error)

	ListByOptions(questionID QuestionUUID, offset, limit uint64) (options []QuestionOptionUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuestionOptions_AlgorithmType uint8

const (
	QuestionOptions_AlgorithmType_Unset QuestionOptions_AlgorithmType = iota
	QuestionOptions_AlgorithmType_UserID
	QuestionOptions_AlgorithmType_StaffID
	QuestionOptions_AlgorithmType_RegisteredTime
)

type QuestionOptions_Type uint16

const (
	QuestionOptions_Type_Unset    QuestionOptions_Type = 0
	QuestionOptions_Type_DropList QuestionOptions_Type = (1 << iota)
)
