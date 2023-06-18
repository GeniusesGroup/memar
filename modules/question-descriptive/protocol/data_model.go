/* For license and copyright information please see the LEGAL file in the code repository */

package qdp

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID    //
	Type() Type                     //
	Min() uint64                    //
	Max() uint64                    //
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_Text
	Type_Textarea

	Type_Color

	Type_Date
	Type_Time
	Type_Year
	Type_Month
	Type_Week

	Type_Password
	Type_Email
	Type_TelNumber
	Type_URL
	Type_File

	Type_Number
	Type_Number_Decimal
	Type_NumberRange
)
