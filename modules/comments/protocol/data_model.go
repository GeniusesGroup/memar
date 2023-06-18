/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	
	er "libgo/error"
	cp "org/modules/comment/protocol"
)

type Comments_GUI_Page_Conditions interface {
	UserID()
}

type Comments_GUI_Page_Services interface {
	Filter() (err protocol.Error)
}

var (
	ErrAccessIsDenied er.Error
)
