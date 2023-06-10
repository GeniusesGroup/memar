/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// Individual and General score
type FinancialScore interface {
	UserID() up.UserUUID            //
	Score() int64                   //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type FinancialScore_StorageServices interface {
	Save(dm FinancialScore) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, vo protocol.VersionOffset) (dm FinancialScore, nv protocol.NumberOfVersion, err protocol.Error)
}
