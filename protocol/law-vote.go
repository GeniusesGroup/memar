/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// LawVote indicate the domain record data fields.
type LawVote interface {
	LawID() LawUUID                 //
	UserID() UserUUID               //
	Vote() LawVote_Type             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type LawVote_StorageServices interface {
	Save(lv LawVote) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(lawID LawUUID, userID UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(lawID LawUUID, userID UserUUID, vo protocol.VersionOffset) (lv LawVote, nv protocol.NumberOfVersion, err protocol.Error)

	ListUsers(lawID LawUUID, offset, limit uint64) (userIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListLaws(userID UserUUID, offset, limit uint64) (lawIDs []LawUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type LawVote_Type uint8

const (
	LawVote_Type_Unset LawVote_Type = iota
	LawVote_Type_Abstention
	LawVote_Type_Agree
	LawVote_Type_Disagree
)
