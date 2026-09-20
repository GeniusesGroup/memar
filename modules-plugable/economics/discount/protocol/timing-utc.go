/* For license and copyright information please see the LEGAL file in the code repository */

package discount

import (
	"memar/time/earth"
)

type TimingUTC interface {
	Weekdays() earth.Weekdays // what days in weekday in utc time week allow to use this discount
	DayHours() earth.DayHours // what hours in day in utc time week allow to use this discount
}
