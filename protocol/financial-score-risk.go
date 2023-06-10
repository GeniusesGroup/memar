/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// FinancialRiskScore
// Store user risk to prevent or detect frauds
type FinancialRiskScore interface {
	UserID() up.UserUUID            //
	Score() int64                   //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type FinancialRiskScore_StorageServices interface {
	Save(dm FinancialRiskScore) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, vo protocol.VersionOffset) (dm FinancialRiskScore, nv protocol.NumberOfVersion, err protocol.Error)
}
