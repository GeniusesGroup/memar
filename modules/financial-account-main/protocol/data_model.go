/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// FinancialAccountMain indicate the domain record data fields.
type FinancialAccountMain interface {
	UserID() up.UserUUID             //
	Currency() FinancialCurrencyUUID 
	AccountID() FinancialAccountUUID 
	Time() protocol.Time             // save time
	RequestID() urp.UserRequestUUID  //
}

type FinancialAccountMain_StorageServices interface {
	Save(dm FinancialAccountMain) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID, currency FinancialCurrencyUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, currency FinancialCurrencyUUID, vo protocol.VersionOffset) (dm FinancialAccountMain, nv protocol.NumberOfVersion, err protocol.Error)
}
