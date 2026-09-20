/* For license and copyright information please see the LEGAL file in the code repository */

package fcpp

import (
	container_p "memar/computer/adt/container/protocol"

	user_p "org/modules/identity/user/protocol"
	label_p "org/modules/knowledge/label/protocol"
)

type GUI_Page_HyperLinks interface {
	NavigateToUserPage()
}

// /friendship_cycle?uid=uuuuuuu&ur=1&o=1&l=20
type GUI_Page_Conditions interface {
	user_p.Field_UserUUID
	label_p.Field_LabelUUID

	container_p.Pagination_Offset_Request
}

type GUI_Page_Service interface {
	DeleteUser()
	MoveUser()

	ShowFriendshipCycleList(relationType label_p.UUID)

	ChangeViewLayout()
	JumpToRootList()
	JumpToLastList()
	LoadMoreUp()
	LoadMoreDown()
}
