/* For license and copyright information please see the LEGAL file in the code repository */

package errs

import (
	er "memar/error"
	"memar/errors"
	error_p "memar/process/error/protocol"
)

var ErrGuestConnectionMaxReached errGuestConnectionMaxReached

type errGuestConnectionMaxReached struct{ er.Err }

func (dt *errGuestConnectionMaxReached) Init() (err error_p.Error) {
	err = dt.Err.Init(domainBaseMediatype + "name=guest-connection-max-reached")
	if err != nil {
		return
	}
	err = errors.Register(dt)
	return
}
