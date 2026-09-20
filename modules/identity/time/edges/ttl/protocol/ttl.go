/* For license and copyright information please see the LEGAL file in the code repository */

package ttl_p

import (
	"memar/time/duration"
)

// TTL(Time-To-Live) or Expiration Number of nanoseconds until record expires.
type TTL interface {
	TTL() duration.NanoSecond
}
