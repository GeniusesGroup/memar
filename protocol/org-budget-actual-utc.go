/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/utc"
)

// OrgProfit
// https://en.wikipedia.org/wiki/Rate_of_profit
type OrgBudgetActualUTC interface {
	Week() utc.WeekElapsed         //
	Income() protocol.MoneyAmount  //
	Outcome() protocol.MoneyAmount //
	Time() protocol.Time           // save time
	RequestID() UserRequestUUID    // user-request domain
}

// Usage:
// - Shareholders can see org profit and decide to sell or buy more stocks.
// - Country Governments: need to steal organizations profits by the name of law as Tax, ...! so force them to implement these services.
// - Stock Markets: need to show related data to traders to know the quality of organizations in making profit.
const (
	ProfitDomain = "profit.protocol"

	ProfitRateURN = "urn:giti:sabz.city:service:profit-rate"

	ProfitServiceBaseCurrency     = "urn:giti:profit.protocol:service:base-currency"
	ProfitServiceAllCurrency      = "urn:giti:profit.protocol:service:all-currency"
	ProfitServiceSpecificCurrency = "urn:giti:profit.protocol:service:specific-currency" // for each day
	// ProfitService              = "urn:giti:profit.protocol:service:"
)

type ProfitServiceBaseCurrencyResponse interface {
	BaseCurrency() uint32 // same as SocietyID in GP protocol
}

type ProfitServiceAllCurrencyRequest interface {
	Time() protocol.Time // it will round to a day and return profit for the day.
}
type ProfitServiceAllCurrencyResponse interface {
	Amount() int64 // in the base currency
}
