/* For license and copyright information please see the LEGAL file in the code repository */

package udp

import (
	"libgo/protocol"

	up "org/modules/user/protocol"
)

type (
	BS_Register_Request interface {
		Domain() string
		UserID() up.UserUUID // TODO::: get user id from connection??
	}
)

type (
	BS_Count_Request interface {
		Domain() string
	}
	BS_Count_Response interface {
		Numbers() uint64
	}
)

type (
	BS_Get_Request interface {
		Domain() string
		VersionOffset() protocol.VersionOffset
	}
	BS_Get_Response1 = DataModel
	BS_Get_Response2 protocol.NumberOfVersion
)

type (
	BS_FindByUserID_Request interface {
		UserID() up.UserUUID
		protocol.Pagination
	}
	BS_FindByUserID_Response interface {
		Domains() []string
		Numbers() uint64
	}
)

// Admins services

type (
	BS_ChangeStatus_Request interface {
		Domain() string
		Status() Status
	}
)
