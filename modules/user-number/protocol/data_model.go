/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// TODO::: need domain or any fields here to support for Numbers Authority (GOD mode)? e.g. [IANA](https://iana.org/)

type UserNumber interface {
	UserID() up.UserUUID //
	OrgID() OrgUUID      //
	ProviderID() OrgUUID //
	Number() string      // like PhoneNumber
	// Number() uint64          // without country code e.g. {(00)98-}912-345-6789
	Status() UserNumber_Status      //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID // Request RecordID to prove how this object created in the chain of other objects.
}

type UserNumber_StorageServices interface {
	Save(pn UserNumber) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID, orgID OrgUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, orgID OrgUUID, vo protocol.VersionOffset) (pn UserNumber, nv protocol.NumberOfVersion, err protocol.Error)

	FindByNumber(number uint64, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

// UserNumber_Status indicate UserNumber record status
type UserNumber_Status Quiddity_Status

const (
	Product_Status_Approved = Product_Status(Quiddity_Status_FreeFlag << iota)
	// UserNumber_Status_Hidden		in this case user can't login by number
)

/*
	Business Services
*/

type (
	UserNumber_Service_Register_Request interface {
		OrgID() up.UserUUID
		Number() string
	}
)
type (
	UserNumber_Service_Count_Request interface {
		UserID() up.UserUUID
		OrgID() up.UserUUID
	}
	UserNumber_Service_Count_Response = protocol.NumberOfVersion
)
type (
	UserNumber_Service_Get_Request interface {
		UserID() up.UserUUID
		OrgID() up.UserUUID
		VersionOffset() protocol.VersionOffset
	}
	UserNumber_Service_Get_Response = UserNumber
)
type (
	UserNumber_Service_SendVerification_Request interface {
		Number() string
	}
)
type (
	UserNumber_Service_Verify_Request interface {
		Number() string
		Token() string
	}
)
type (
	UserNumber_Service_IsVerified_Request interface {
		Number() string
	}
	UserNumber_Service_IsVerified_Response interface {
		Verified() bool
	}
)
type (
	UserNumber_Service_IsExist_Request interface {
		Number() string
	}
	UserNumber_Service_IsExist_Response interface {
		Exist() bool
	}
)

/*
	Errors
*/
