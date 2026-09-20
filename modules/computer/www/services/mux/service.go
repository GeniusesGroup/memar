/* For license and copyright information please see the LEGAL file in the code repository */

package hs

import (
	errs "memar/net/http/errors"
	http_p "memar/net/http/protocol"
	net_p "memar/net/protocol"
	"memar/process/service"
	error_p "memar/process/error/protocol"
)

// Service implement protocol.Service when embed to other struct that implements other needed methods.
type Service struct {
	service.Service
}

//memar:impl memar/net/http/protocol.Handler
func (s *Service) URI() string { return "" }
func (s *Service) ServeHTTP(sk net_p.Socket, httpReq http_p.Request, httpRes http_p.Response) (err error_p.Error) {
	err = &errs.ErrServiceNotAcceptHTTP
	return
}
