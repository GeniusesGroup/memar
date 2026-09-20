/* For license and copyright information please see the LEGAL file in the code repository */

package pcp

import (
	error_p "memar/process/error/protocol"

	user_p "org/modules/identity/user/protocol"
)

type Comments_GUI_Page_Conditions interface {
	user_p.Field_UserUUID
}

type Comments_GUI_Page_Services interface {
	Filter() (err error_p.Error)
}
