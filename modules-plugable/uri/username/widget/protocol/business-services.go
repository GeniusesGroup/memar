/* For license and copyright information please see the LEGAL file in the code repository */

package un_p

import (
	container_p "memar/computer/adt/container/protocol"

	storage_p "memar/storage/protocol"
	org_p "org/modules/identity/organization/protocol"
	user_p "org/modules/identity/user/protocol"
)

type (
	BS_Register_Request interface {
		user_p.Field_UserUUID // TODO::: get user id from connection??
		Field_Username
	}
)

type (
	BS_Count_Request interface {
		user_p.Field_UserUUID
	}
	BS_Count_Response = storage_p.NumberOfVersion
)

type (
	BS_Get_Request interface {
		user_p.Field_UserUUID
	}
	BS_Get_Response = DataModel
)

type (
	BS_FindByUsername_Request interface {
		Field_Username
		container_p.Pagination_Offset_Request
	}
	BS_FindByUsername_Response interface {
		UserIDs() []user_p.UUID
		container_p.Pagination_Response
	}
)

// Use to send verification token by email protocol to other organization software to verify username manually.
type (
	BS_SendManualVerification_Request interface {
		user_p.Field_UserUUID
		org_p.Field_OrganizationID
		Field_Username
		ProtocolType() string
	}
)
type (
	BS_VerifyManually_Request interface {
		user_p.Field_UserUUID
		org_p.Field_OrganizationID
		Field_Username
		Token() string
	}
)

// Admins services

type (
	BS_ChangeStatus_Request interface {
		Field_Username
		// Field_Status
	}
)
