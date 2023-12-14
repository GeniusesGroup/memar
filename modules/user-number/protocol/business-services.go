/* For license and copyright information please see the LEGAL file in the code repository */

package unp

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

type (
	BS_Register_Request interface {
		OrgID() up.UserUUID
		Number() Number
	}
)

type (
	BS_Count_Request interface {
		UserID() up.UserUUID
		OrgID() up.UserUUID
	}
	BS_Count_Response = protocol.NumberOfVersion
)

type (
	BS_Get_Request interface {
		UserID() up.UserUUID
		OrgID() up.UserUUID
		VersionOffset() protocol.VersionOffset
	}
	BS_Get_Response = DataModel
)

type (
	BS_SendVerification_Request interface {
		Number() Number
	}
)

type (
	BS_Verify_Request interface {
		Number() Number
		Token() string
	}
)

type (
	BS_IsVerified_Request interface {
		Number() Number
	}
	BS_IsVerified_Response interface {
		Verified() bool
	}
)

type (
	BS_IsExist_Request interface {
		Number() Number
	}
	BS_IsExist_Response interface {
		Exist() bool
	}
)
