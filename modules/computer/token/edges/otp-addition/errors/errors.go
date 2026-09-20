/* For license and copyright information please see the LEGAL file in the code repository */

package otp

import (
	er "memar/error"
)

// Errors
var (
	ErrWrongNumber er.Error
)

func init() {
	ErrWrongNumber.Init("domain/memar.scm.geniuses.group; package=otp; type=error; name=wrong-number")
}
