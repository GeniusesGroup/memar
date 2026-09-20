/* For license and copyright information please see the LEGAL file in the code repository */

package errs

import (
	er "memar/error"
	"memar/errors"
)

var ErrProtocolHandler errProtocolHandler

type errProtocolHandler struct{ er.Err }

func (dt *errProtocolHandler) Init() (err error_p.Error) {
	err = dt.Err.Init(domainBaseMediatype + "name=protocol-handler")
	if err != nil {
		return
	}
	err = errors.Register(dt)
	return
}
