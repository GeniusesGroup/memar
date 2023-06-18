/* For license and copyright information please see the LEGAL file in the code repository */

package gap

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
	gp "org/modules/group/protocol"
)

// DataModel indicate the domain record data fields
type DataModel interface {
	GroupID() gp.GroupUUID            //
	UserID() up.UserUUID              //
	JoinBy() up.UserUUID              //
	JoinWay() GroupAssociated_JoinWay //
	SaveTime() protocol.Time          //
	RequestID() urp.UserRequestUUID   //
}


type GroupAssociated_JoinWay uint8

const (
	GroupAssociated_JoinWay_Unset GroupAssociated_JoinWay = iota
	GroupAssociated_JoinWay_Direct
	GroupAssociated_JoinWay_JoinLink
	GroupAssociated_JoinWay_Invite
)
