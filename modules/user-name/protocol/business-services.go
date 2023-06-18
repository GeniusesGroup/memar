/* For license and copyright information please see the LEGAL file in the code repository */

package unp

import (
	"libgo/protocol"

	up "org/modules/user/protocol"
)

/*
	Business Services
*/

type (
	UserName_Service_Register_Request interface {
		UserID() up.UserUUID // TODO::: get user id from connection??
		Username() string
	}
)

type (
	UserName_Service_Count_Request interface {
		UserID() up.UserUUID
	}
	UserName_Service_Count_Response = protocol.NumberOfVersion
)

type (
	UserName_Service_Get_Request interface {
		UserID() up.UserUUID
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
		UserIDs() []up.UserUUID
		Numbers() uint64
	}
)

// Use to send verification token by email protocol to other organization software to verify username manually.
type (
	UserName_Service_SendManualVerification_Request interface {
		UserID() up.UserUUID
		OrgID() up.UserUUID
		Username() string
		ProtocolType() string
	}
)
type (
	UserName_Service_VerifyManually_Request interface {
		UserID() up.UserUUID
		OrgID() up.UserUUID
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
