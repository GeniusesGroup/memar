/* For license and copyright information please see the LEGAL file in the code repository */

package upp

import (
	urup "org/modules/user-relation-user/protocol"
	up "org/modules/user/protocol"
)

type GUI_Page_UsedDomains interface {
	// Staff
	// Content
	// User
	// Group
	// List
	// Timeline
	// Quiddity

	// TODO:::
	// AccessibilityStatus
	// OnlineStatus
}

type GUI_Page_HyperLinks interface {
	NavigateToFriendshipCyclePage()
}

type GUI_Page_Conditions interface {
	UserID() up.UserUUID //
}

type GUI_Page_Service interface {
	ChangeViewLayout()
	// Block()
	Report()
	SetNotifyType(nt Notify_Type)

	RSSFeed()

	// Same as follow
	AddToFriendshipCycle(uid up.UserUUID, r urup.User_Relation)
}

type Notify_Type uint8

const (
	Notify_Type_Unset Notify_Type = iota
	Notify_Type_Casual
	Notify_Type_All
	Notify_Type_Mute
)
