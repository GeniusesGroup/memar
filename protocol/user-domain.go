/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type UserDomain interface {
	Domain() string             // unique name in the computer world
	UserID() protocol.UserID    // user domain
	Status() UserDomain_Status  //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type UserDomain_StorageServices interface {
	Save(ud UserDomain) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(domain string) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(domain string, vo protocol.VersionOffset) (ud UserDomain, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUserID(userID [16]byte, offset, limit uint64) (domains []string, nv protocol.NumberOfVersion, err protocol.Error)
}

// UserDomain_Status indicate UserDomain record status
type UserDomain_Status Quiddity_Status

// UserDomain statuses
const (
// UserDomain_Status_ = UserDomain_Status(Quiddity_Status_FreeFlag << iota)
)

/*
	Business Services
*/

type UserDomain_Service_Register_Request interface {
	Domain() string
	UserID() protocol.UserID // TODO::: get user id from connection??
}

type UserDomain_Service_Count_Request interface {
	Domain() string
}
type UserDomain_Service_Count_Response interface {
	Numbers() uint64
}

type UserDomain_Service_Get_Request interface {
	Domain() string
	VersionOffset() protocol.VersionOffset
}
type UserDomain_Service_Get_Response1 interface {
	UserDomain
}
type UserDomain_Service_Get_Response2 protocol.NumberOfVersion

type UserDomain_Service_FindByUserID_Request interface {
	UserID() protocol.UserID
	Offset() uint64
	Limit() uint64
}
type UserDomain_Service_FindByUserID_Response interface {
	Domains() []string
	Numbers() uint64
}

// Admins services

type UserDomain_Service_ChangeStatus_Request interface {
	Domain() string
	Status() UserDomain_Status
}

/*
	Errors
*/
