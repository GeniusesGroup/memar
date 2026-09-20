/* For license and copyright information please see the LEGAL file in the code repository */

package gds

import (
	"memar/net/http"
	http_p "memar/net/http/protocol"
	"memar/net/srpc"
	error_p "memar/process/error/protocol"
	"memar/protocol"
)

func (ser *serv) ServeSRPC(st protocol.Socket, rawReq protocol.Codec) (rawRes protocol.Codec, err error_p.Error) {
	var req = &Request{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *getServiceDetailRes
	res, err = getServiceDetail(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = res.Syllab
	return
}

func (ser *serv) ServeHTTP(st protocol.Socket, httpReq http_p.Request, httpRes protocol.HTTPResponse) (err error_p.Error) {
	var req Request
	_, err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *getServiceDetailRes
	res, err = getServiceDetail(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(res.JSON)
	return
}
