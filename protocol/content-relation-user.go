/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// ContentParticipant indicate the domain record data fields.
type ContentParticipant interface {
	ContentID() ContentUUID         //
	UserID() up.UserUUID            //
	Type() ContentParticipant_Type  //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

// TODO::: immutable?? if wrong data save for a content??
type ContentParticipant_StorageServices interface {
	Save(dm ContentParticipant) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID ContentUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID ContentUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm ContentParticipant, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ContentIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (contentIDs []ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_UserIDs_BY_ContentID(contentID ContentUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

// ContentParticipant_Type indicate participant type or role
type ContentParticipant_Type uint32

// ContentParticipant types
const (
	ContentParticipant_Type_Unset ContentParticipant_Type = iota

	// Content_Type_Music
	ContentParticipant_Type_SongWriter
	ContentParticipant_Type_Composer
	ContentParticipant_Type_Regulator
	ContentParticipant_Type_MusicSupplier

	// Content_Type_Movie
	ContentParticipant_Type_Director

	// Content_Type_Game
	ContentParticipant_Type_SportTeam
)


// 	FIND_ContentIDs_BY_UserID_AND_Type(userID up.UserUUID, t ContentParticipant_Type, offset, limit uint64) (contentIDs []ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)
