/* For license and copyright information please see LEGAL file in repository */

package services

import (
	"github.com/GeniusesGroup/libgo/http"
	"github.com/GeniusesGroup/libgo/json"
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/srpc"
)

func (ser *get) ServeSRPC(st protocol.Stream) (err protocol.Error) {
	// TODO::: auto generate
	var req = &GetRequest{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *getQuiddityRes
	res, err = ser.Process(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
	return
}

func (ser *get) ServeHTTP(st protocol.Stream, httpReq protocol.HTTPRequest, httpRes protocol.HTTPResponse) (err protocol.Error) {
	// TODO::: auto generate
	var req = &GetRequest{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *getQuiddityRes
	res, err = ser.Process(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
	return
}
