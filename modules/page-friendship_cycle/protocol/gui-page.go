/* For license and copyright information please see the LEGAL file in the code repository */

package fcpp

import (
	"libgo/protocol"

	urup "org/modules/user-relation-user/protocol"
	up "org/modules/user/protocol"
)

type GUI_Page_UsedDomains interface {
	// User
	// Quiddity
}

type GUI_Page_HyperLinks interface {
	NavigateToUserPage()
}

// /friendship_cycle?uid=uuuuuuu&ur=1&o=1&l=20
type GUI_Page_Conditions interface {
	UserID() up.UserUUID              //
	RelationType() urup.User_Relation //

	protocol.Pagination
}

type GUI_Page_Service interface {
	DeleteUser()
	MoveUser()

	ShowFriendshipCycleList(r urup.User_Relation)

	ChangeViewLayout()
	JumpToRootList()
	JumpToLastList()
	LoadMoreUp()
	LoadMoreDown()
}
