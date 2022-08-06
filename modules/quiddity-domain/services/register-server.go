/* For license and copyright information please see LEGAL file in repository */

package services

import (
	"github.com/GeniusesGroup/libgo/ganjine"
	"github.com/GeniusesGroup/libgo/http"
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/service"
	"github.com/GeniusesGroup/libgo/srpc"
	dp "github.com/GeniusesGroup/organization/modules/quiddity-domain/protocol"
)

func (ser *registerService) ServeSRPC(st protocol.Stream) (err protocol.Error) {
	var req RegisterRequest
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	err = ser.Process(st, &req)
	return
}
func (ser *registerService) ServeHTTP(st protocol.Stream, httpReq protocol.HTTPRequest, httpRes protocol.HTTPResponse) (err protocol.Error) {
	var req RegisterRequest
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	err = ser.Process(st, &req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	return
}
