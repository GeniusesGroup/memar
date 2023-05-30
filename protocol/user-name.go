/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserName indicate the domain record data fields.
// it is use in many other services like send email(email address), ...
type UserName interface {
	UserID() UserUUID               //
	OrgID() OrgUUID                 //
	Username() string               // It is not replace of user ID. It usually use to find user by their friends in more human friendly manner.
	Status() UserName_Status        //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type UserName_StorageServices interface {
	Save(un UserName) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID, orgID UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID, orgID UserUUID, vo protocol.VersionOffset) (un UserName, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUsername(username string, offset, limit uint64) (userIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	ListOrgs(userID UserUUID, offset, limit uint64) (orgIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

// UserName_Status indicate UserName record status
type UserName_Status Quiddity_Status

// UserName status
const (
	UserName_Status_Reserved = UserName_Status(Quiddity_Status_FreeFlag << iota)
)

/*
	Business Services
*/

type (
	UserName_Service_Register_Request interface {
		UserID() UserUUID // TODO::: get user id from connection??
		Username() string
	}
)

type (
	UserName_Service_Count_Request interface {
		UserID() UserUUID
	}
	UserName_Service_Count_Response = protocol.NumberOfVersion
)

type (
	UserName_Service_Get_Request interface {
		UserID() UserUUID
		VersionOffset() protocol.VersionOffset
	}
	UserName_Service_Get_Response1 = UserName
	UserName_Service_Get_Response2 = protocol.NumberOfVersion
)

type (
	UserName_Service_FindByUsername_Request interface {
		Username() string
		Offset() uint64
		Limit() uint64
	}
	UserName_Service_FindByUsername_Response interface {
		UserIDs() []UserUUID
		Numbers() uint64
	}
)

// Use to send verification token by email protocol to other organization software to verify username manually.
type (
	UserName_Service_SendManualVerification_Request interface {
		UserID() UserUUID
		OrgID() UserUUID
		Username() string
		ProtocolType() string
	}
)
type (
	UserName_Service_VerifyManually_Request interface {
		UserID() UserUUID
		OrgID() UserUUID
		Username() string
		Token() string
	}
)

// Admins services

type (
	UserName_Service_ChangeStatus_Request interface {
		Username() string
		Status() UserName_Status
	}
)

/*
	Errors
*/

const (
// UserName_Error_ = "domain/username.protocol; type=error; name="
)
