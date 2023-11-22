/* For license and copyright information please see the LEGAL file in the code repository */

package cpp

import (
	cp "org/modules/comment/protocol"
)

type GUI_Widget_Conditions interface {
	CommentID() cp.CommentUUID
}

type GUI_Widget_Service interface {
	NavigateToUserInfo()
}
