/* For license and copyright information please see the LEGAL file in the code repository */

package usacuhp

import (
	"memar/time/utc"

	usp "org/modules/identity/user-sexuality/protocol"
)

type DataModel interface {
	utc.Field_HourElapsed
	Sexuality() usp.Sexuality
	Count() Count
}
