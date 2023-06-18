/* For license and copyright information please see the LEGAL file in the code repository */

package gpp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	GroupID() gp.GroupUUID             //
	GetPolicy() GroupPolicy_Policy     // Visibility level
	SetPolicy() GroupPolicy_Policy     //
	ForwardPolicy() GroupPolicy_Policy //
	SaveTime() protocol.Time           //
	RequestID() urp.UserRequestUUID    //
}

type GroupPolicy_Policy uint16

const (
	GroupPolicy_Policy_Unset     GroupPolicy_Policy = 0
	GroupPolicy_Policy_JustOwner GroupPolicy_Policy = (1 << iota)
	GroupPolicy_Policy_GroupManagers
	GroupPolicy_Policy_GroupMembers
	GroupPolicy_Policy_Mentioned
	GroupPolicy_Policy_AnyOne
	// Below policies are person type authorization
	GroupPolicy_Policy_1stFriendshipCycle
	GroupPolicy_Policy_2stFriendshipCycle
	GroupPolicy_Policy_3stFriendshipCycle
	GroupPolicy_Policy_4stFriendshipCycle
	GroupPolicy_Policy_5stFriendshipCycle
	GroupPolicy_Policy_6stFriendshipCycle
)
