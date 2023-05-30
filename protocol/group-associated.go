/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// GroupAssociated indicate the domain record data fields
type GroupAssociated interface {
	GroupID() GroupUUID               //
	UserID() up.UserUUID              //
	JoinBy() up.UserUUID              //
	JoinWay() GroupAssociated_JoinWay //
	Time() protocol.Time              // save time
	RequestID() urp.UserRequestUUID   //
}

type GroupAssociated_JoinWay uint8

const (
	GroupAssociated_JoinWay_Unset GroupAssociated_JoinWay = iota
	GroupAssociated_JoinWay_Direct
	GroupAssociated_JoinWay_JoinLink
	GroupAssociated_JoinWay_Invite
)
