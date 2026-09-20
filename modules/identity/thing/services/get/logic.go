/* For license and copyright information please see the LEGAL file in the code repository */

package get

import (
	"libgo/protocol"

	"org/modules/quiddity-domain/internal/storage"
	qdp "org/modules/quiddity-domain/protocol"
)

func (s *ser) Process(st protocol.Stream, req qdp.Service_Get_Request) (res qdp.Service_Get_Response, err protocol.Error) {
	err = s.authorize(st)
	if err != nil {
		return
	}

	res, err = storage.Storage.Get(req.QuiddityID())
	return
}

func (s *ser) authorize(st protocol.Stream) (err protocol.Error) {
	err = st.Authorize()
	// TODO::: authorization??
	// TODO::: auto generate??
	return
}

func (s *ser) validateRequest(req qdp.Service_Get_Request) (err protocol.Error) {
	// TODO::: auto generate
	return
}
