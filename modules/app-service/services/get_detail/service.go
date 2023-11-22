/* For license and copyright information please see the LEGAL file in the code repository */

package gds

import (
	"memar/net/srpc"
	"memar/protocol"
	"memar/service"
	"memar/services"
)

var Service serv

// var GetServiceDetailService = serv{
// 	Service: New("domain/service.protocol.service; name=get-service-detail", "", protocol.Software_PreAlpha, 1601109351).
// 		SetDetail(protocol.LanguageEnglish, "Get Service Detail",
// 			"Returns service all details by given service ID or URI",
// 			[]string{}).
// 		SetAuthorization(protocol.CRUDRead, protocol.UserType_All).Expired(0, ""),
// }

type serv struct {
	service.Service
}

func (ser *serv) DO(st protocol.Socket, req *Request) (res *Response, err protocol.Error) {
	var reqService *service.Service
	if req.ServiceID != 0 {
		reqService, err = services.GetByID(req.ServiceID)
	} else {
		reqService, err = protocol.App.GetServiceByURI(req.ServiceURI)
	}

	if reqService == nil {
		err = srpc.ErrServiceNotFound
	} else {
		res = &Response{
			JSON:   reqService.JSON,
			Syllab: reqService.Syllab,
		}
	}
	return
}

func (ser *serv) DoSRPC(req Request) (res Response, err protocol.Error) {
	return
}

func (ser *serv) DoHTTP(req Request) (res Response, err protocol.Error) {
	return
}
