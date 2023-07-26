/* For license and copyright information please see the LEGAL file in the code repository */

package unp

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

type (
	BS_Register_Request interface {
		UserID() up.UserUUID // TODO::: get user id from connection??
		Username() Username
	}
)

type (
	BS_Count_Request interface {
		UserID() up.UserUUID
	}
	BS_Count_Response = protocol.NumberOfVersion
)

type (
	BS_Get_Request interface {
		UserID() up.UserUUID
		VersionOffset() protocol.VersionOffset
	}
	BS_Get_Response1 = DataModel
	BS_Get_Response2 = protocol.NumberOfVersion
)

type (
	BS_FindByUsername_Request interface {
		Username() Username
		protocol.Pagination
	}
	BS_FindByUsername_Response interface {
		UserIDs() []up.UserUUID
		Numbers() uint64
	}
)

// Use to send verification token by email protocol to other organization software to verify username manually.
type (
	BS_SendManualVerification_Request interface {
		UserID() up.UserUUID
		OrgID() up.UserUUID
		Username() Username
		ProtocolType() string
	}
)
type (
	BS_VerifyManually_Request interface {
		UserID() up.UserUUID
		OrgID() up.UserUUID
		Username() Username
		Token() string
	}
)

// Admins services

type (
	BS_ChangeStatus_Request interface {
		Username() Username
		Status() Status
	}
)
