/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// UserName indicate the domain record data fields.
// it is use in many other services like send email(email address), ...
type UserName interface {
	UserID() protocol.UserID    // user domain
	OrgID() protocol.UserID     // user domain. TenantID
	Username() string           // It is not replace of user ID. It usually use to find user by their friends in more human friendly manner.
	Status() UserName_Status    //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type UserName_StorageServices interface {
	Save(un UserName) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID, orgID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID, orgID [16]byte, vo protocol.VersionOffset) (un UserName, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUsername(username string, offset, limit uint64) (userIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	ListOrgs(userID [16]byte, offset, limit uint64) (orgIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

// UserName_Status indicate UserName record status
type UserName_Status = Quiddity_Status

// UserName status
const (
	UserName_Status_Reserved = UserName_Status(Quiddity_Status_FreeFlag << iota)
)

/*
	Business Services
*/

type (
	UserName_Service_Register_Request interface {
		UserID() protocol.UserID // TODO::: get user id from connection??
		Username() string
	}
)

type (
	UserName_Service_Count_Request interface {
		UserID() protocol.UserID
	}
	UserName_Service_Count_Response = protocol.NumberOfVersion
)

type (
	UserName_Service_Get_Request interface {
		UserID() protocol.UserID
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
		UserIDs() [][16]byte
		Numbers() uint64
	}
)

// Use to send verification token by email protocol to other organization software to verify username manually.
type (
	UserName_Service_SendManualVerification_Request interface {
		UserID() protocol.UserID
		OrgID() protocol.UserID
		Username() string
		ProtocolType() string
	}
)
type (
	UserName_Service_VerifyManually_Request interface {
		UserID() protocol.UserID
		OrgID() protocol.UserID
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
