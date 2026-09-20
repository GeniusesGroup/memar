/* For license and copyright information please see the LEGAL file in the code repository */

package errs

import (
	er "memar/error"
	"memar/errors"
	error_p "memar/process/error/protocol"
)

var ErrInternalError errInternalError

type errInternalError struct{ er.Err }

func (dt *errInternalError) Init() (err error_p.Error) {
	err = dt.Err.Init(domainBaseMediatype + "name=internal-error")
	if err != nil {
		return
	}
	err = errors.Register(dt)
	return
}
