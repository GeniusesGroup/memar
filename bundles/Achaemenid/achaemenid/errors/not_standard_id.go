/* For license and copyright information please see the LEGAL file in the code repository */

package errs

import (
	er "memar/error"
	"memar/errors"
)

var ErrNotStandardID errNotStandardID

type errNotStandardID struct{ er.Err }

func (dt *errNotStandardID) Init() (err error_p.Error) {
	err = dt.Err.Init(domainBaseMediatype + "name=not-standard-id")
	if err != nil {
		return
	}
	err = errors.Register(dt)
	return
}
