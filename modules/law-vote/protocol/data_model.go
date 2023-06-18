/* For license and copyright information please see the LEGAL file in the code repository */

package lvp

import (
	"libgo/protocol"

	lp "org/modules/law/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	LawID() lp.LawUUID              //
	UserID() up.UserUUID            //
	Vote() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	LawVote_Type_Unset Type = iota
	LawVote_Type_Abstention
	LawVote_Type_Agree
	LawVote_Type_Disagree
)
