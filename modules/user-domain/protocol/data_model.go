/* For license and copyright information please see the LEGAL file in the code repository */

package udp

import (
	"libgo/protocol"

	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel is unique name in the computer world. Country e.g. Iran, ... || Digital platforms e.g. Instagram, Facebook, Google, Github, Yahoo, ...
type DataModel interface {
	Domain() string                   // unique name in the computer world
	UserID() up.UserUUID              //
	AcceptedProtocols() UserDomain_AP //
	Status() Status                   //
	SaveTime() protocol.Time          //
	RequestID() urp.UserRequestUUID   //
}

// UserDomain_AP is user domain accepted protocols
type UserDomain_AP uint8

const (
	UserDomain_AP_Unset UserDomain_AP = iota
	UserDomain_AP_Email
	UserDomain_AP_SMS
	UserDomain_AP_PhoneCall
)

// Status indicate UserDomain record status
type Status qsp.Quiddity_Status

// UserDomain statuses
const (
// Status_ = Status(Quiddity_Status_FreeFlag << iota)
)



/*
	Errors
*/
