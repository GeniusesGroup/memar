/* For license and copyright information please see the LEGAL file in the code repository */

package group_authorization

type Policy uint16

const (
	Policy_Unset     Policy = 0
	Policy_JustOwner Policy = (1 << iota)
	Policy_GroupManagers
	Policy_GroupMembers
	Policy_Mentioned
	Policy_AnyOne
	// Below policies are person type authorization
	Policy_1stFriendshipCycle
	Policy_2stFriendshipCycle
	Policy_3stFriendshipCycle
	Policy_4stFriendshipCycle
	Policy_5stFriendshipCycle
	Policy_6stFriendshipCycle
)
