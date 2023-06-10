/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// OrgSalaryUTC is fixed salary that use in roles salary rules to calculate each staff salary.
type OrgSalaryUTCWeekly interface {
	OrgID() OrgUUID
	CurrencyID() FinancialCurrencyUUID  //
	Amount() protocol.MoneyAmount       //
	Time() protocol.Time                // save time
	RequestID() urp.UserRequestUUID     //
}

type OrgSalaryUTC_StorageServices interface {
	Save(dm OrgSalaryUTCWeekly) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orgID OrgUUID, currencyID FinancialCurrencyUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orgID OrgUUID, currencyID FinancialCurrencyUUID, vo protocol.VersionOffset) (dm OrgSalaryUTCWeekly, err protocol.Error)
}
