/* For license and copyright information please see the LEGAL file in the code repository */

package pcp

import (
	"memar/protocol"
)

type Comments_GUI_Page_Conditions interface {
	UserID()
}

type Comments_GUI_Page_Services interface {
	Filter() (err protocol.Error)
}
