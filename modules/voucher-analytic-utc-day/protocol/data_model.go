/* For license and copyright information please see the LEGAL file in the code repository */

package vaudp

import (
	"libgo/protocol"
	"libgo/time/utc"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Day() utc.DayElapsed                //
	Issued() uint64                     // Total
	IssuedAmount() protocol.MoneyAmount // Total
	SaveTime() protocol.Time            //
}
