/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// Domain is unique name in the computer world. Country e.g. Iran, ... || Digital platforms e.g. Instagram, Facebook, Google, Github, Yahoo, ...
type UserDomain interface {
	Domain() string                   // unique name in the computer world
	UserID() UserUUID                 //
	AcceptedProtocols() UserDomain_AP //
	Status() UserDomain_Status        //
	Time() protocol.Time              // save time
	RequestID() urp.UserRequestUUID   //
}

type UserDomain_StorageServices interface {
	Save(ud UserDomain) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(domain string) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(domain string, vo protocol.VersionOffset) (ud UserDomain, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUserID(userID UserUUID, offset, limit uint64) (domains []string, nv protocol.NumberOfVersion, err protocol.Error)
}

// UserDomain_AP is user domain accepted protocols
type UserDomain_AP uint8

const (
	UserDomain_AP_Unset UserDomain_AP = iota
	UserDomain_AP_Email
	UserDomain_AP_SMS
	UserDomain_AP_PhoneCall
)

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
	UserID() UserUUID // TODO::: get user id from connection??
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
	UserID() UserUUID
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
