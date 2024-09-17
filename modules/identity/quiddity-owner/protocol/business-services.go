/* For license and copyright information please see the LEGAL file in the code repository */

package qop

import (
	qp "org/modules/quiddity/protocol"
	up "org/modules/user/protocol"
)

type (
	BS_FindByUserID_Request interface {
		UserID() up.UserUUID
		Offset() uint64
		Limit() uint64
	}
	BS_FindByUserID_Response interface {
		QuiddityIDs() []qp.QuiddityUUID
		Numbers() uint64
	}
)
