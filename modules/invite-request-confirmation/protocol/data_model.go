/* For license and copyright information please see the LEGAL file in the code repository */

package ircp

import (
	"libgo/protocol"

	ip "org/modules/invite/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() ip.InviteUUID        //
	AccepterID() up.UserUUID        //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status uint8

const (
	Status_Unset    Status = iota
	Status_OnHold          // GUI base
	Status_Accepted        //
	Status_Rejected        //
	Status_Expired         // GUI base
)
