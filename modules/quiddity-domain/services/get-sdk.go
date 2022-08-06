/* For license and copyright information please see LEGAL file in repository */

package services

import (
	"github.com/GeniusesGroup/libgo/http"
	"github.com/GeniusesGroup/libgo/json"
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/service"
	"github.com/GeniusesGroup/libgo/srpc"

	qdp "github.com/GeniusesGroup/organization/modules/quiddity-domain/protocol"
)

func (ser *get) Do(req qdp.Service_Get_Request) (res qdp.Service_Get_Response, err protocol.Error) {
	err = ser.validateRequest(req)
	if err != nil {
		return nil, err
	}

	// TODO::: auto generate
	return
}

func (ser *get) doSRPC(req qdp.Service_Get_Request) (res qdp.Service_Get_Response, err protocol.Error) {
	// TODO::: auto generate
	return
}

func (ser *get) doHTTP(req qdp.Service_Get_Request) (res qdp.Service_Get_Response, err protocol.Error) {
	// TODO::: auto generate
	return
}
