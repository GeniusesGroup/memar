/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionDescriptive indicate the domain record data fields.
type QuestionDescriptive interface {
	QuestionID() QuestionUUID       //
	Type() QuestionDescriptive_Type //
	Min() uint64                    //
	Max() uint64                    //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionDescriptive_StorageServices interface {
	Save(f QuestionDescriptive) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (f QuestionDescriptive, nv protocol.NumberOfVersion, err protocol.Error)

	FindByType(questionID QuestionUUID, t QuestionDescriptive_Type, offset, limit uint64) (questionIDs []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuestionDescriptive_Type uint8

const (
	QuestionDescriptive_Type_Unset QuestionDescriptive_Type = iota
	QuestionDescriptive_Type_Text
	QuestionDescriptive_Type_Textarea

	QuestionDescriptive_Type_Color

	QuestionDescriptive_Type_Date
	QuestionDescriptive_Type_Time
	QuestionDescriptive_Type_Year
	QuestionDescriptive_Type_Month
	QuestionDescriptive_Type_Week

	QuestionDescriptive_Type_Password
	QuestionDescriptive_Type_Email
	QuestionDescriptive_Type_TelNumber
	QuestionDescriptive_Type_URL
	QuestionDescriptive_Type_File

	QuestionDescriptive_Type_Number
	QuestionDescriptive_Type_Number_Decimal
	QuestionDescriptive_Type_NumberRange
)
