/* For license and copyright information please see the LEGAL file in the code repository */

package usacuhp

import (
	"memar/protocol"
	utc "memar/protocol/time"
	up "org/modules/user/protocol"
	usp "org/modules/user-sexuality/protocol"
)


type DataModel interface {
	Hour() utc.HourElapsed
	Sexuality() usp.Sexuality
	Count() Count
}
