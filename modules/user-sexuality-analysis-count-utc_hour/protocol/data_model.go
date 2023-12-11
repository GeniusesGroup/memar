/* For license and copyright information please see the LEGAL file in the code repository */

package usacuhp

import (
	utc "memar/time/utc"

	usp "org/modules/user-sexuality/protocol"
)

type DataModel interface {
	Hour() utc.HourElapsed
	Sexuality() usp.Sexuality
	Count() Count
}
