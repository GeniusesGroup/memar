/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"libgo/ganjine"
	"libgo/protocol"

	"org/modules/quiddity-domain/internal/storage"
	qdp "org/modules/quiddity-domain/protocol"
)

func (s *ser) Process(st protocol.Stream, req qdp.Service_Register_Request) (err protocol.Error) {
	err = st.Authorize()
	if err != nil {
		return
	}

	if req.URI != "" {
		err = checkQuiddityURI(st, req.URI)
		if err != nil {
			return
		}
	}

	// err = checkOrgName(st, req.Name)
	// if err != nil {
	// 	return
	// }
	// err = checkOrgDomain(st, req.Domain)
	// if err != nil {
	// 	return
	// }

	var q = Quiddity{
		quiddityID: req.QuiddityID(),
		domainID:   req.DomainID(),
		// time: ,
		// requestID:
	}
	err = storage.Storage.Save(&q)
	return
}

func (s *ser) validateRequest(req qdp.Service_Register_Request) (err protocol.Error) {
	// TODO::: auto generate
	return
}

func checkQuiddityURI(st protocol.Stream, uri string) (err protocol.Error) {
	var findQuiddityByURIReq = findQuiddityByURIReq{
		URI:    uri,
		Offset: 18446744073709551615,
		Limit:  1,
	}
	var findQuiddityByURIRes *findQuiddityByURIRes
	findQuiddityByURIRes, err = findQuiddityByURI(st, &findQuiddityByURIReq)
	if err.Equal(ganjine.ErrRecordNotFound) {
		return nil
	}
	if err != nil {
		return
	}

	var getQuiddityLanguagesReq = getQuiddityLanguagesReq{
		ID: findQuiddityByURIRes.IDs[0],
	}
	var getQuiddityLanguagesRes *getQuiddityLanguagesRes
	getQuiddityLanguagesRes, err = getQuiddityLanguages(st, &getQuiddityLanguagesReq)
	if err.Equal(ganjine.ErrRecordNotFound) {
		// TODO::: how it is possible???
		return nil
	}
	if err != nil {
		return
	}

	var getQuiddityReq = getQuiddityReq{
		ID:       findQuiddityByURIRes.IDs[0],
		Language: getQuiddityLanguagesRes.Languages[0],
	}
	var getQuiddityRes *getQuiddityRes
	getQuiddityRes, err = getQuiddity(st, &getQuiddityReq)
	if err.Equal(ganjine.ErrRecordNotFound) {
		// TODO::: how it is possible???
		return nil
	}
	if err != nil {
		return
	}
	if getQuiddityRes.URI == uri {
		return ErrQuiddityURIRegistered
	}
	return
}
