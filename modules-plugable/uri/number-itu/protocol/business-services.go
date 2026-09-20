/* For license and copyright information please see the LEGAL file in the code repository */

package un_p

import (
	storage_p "memar/storage/protocol"
	org_p "org/modules/identity/organization/protocol"
	user_p "org/modules/identity/user/protocol"
)

type (
	BS_Register_Request interface {
		org_p.Field_OrganizationID
		Field_Number
	}
)

type (
	BS_Count_Request interface {
		user_p.Field_UserUUID
		org_p.Field_OrganizationID
	}
	BS_Count_Response = storage_p.NumberOfVersion
)

type (
	BS_Get_Request interface {
		user_p.Field_UserUUID
		org_p.Field_OrganizationID
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
