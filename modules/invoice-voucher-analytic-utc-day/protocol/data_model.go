/* For license and copyright information please see the LEGAL file in the code repository */

package ivaudp

import (
	"libgo/protocol"
	"libgo/time/utc"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Day() utc.DayElapsed                  //
	Redeemed() uint64                     // Total
	RedeemedAmount() protocol.MoneyAmount // Total
	SaveTime() protocol.Time              //
}
