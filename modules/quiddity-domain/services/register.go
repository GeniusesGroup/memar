/* For license and copyright information please see LEGAL file in repository */

package services

import (
	"github.com/GeniusesGroup/libgo/ganjine"
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/service"

	qdp "github.com/GeniusesGroup/organization/modules/quiddity-domain/protocol"
)

var Register register

func init() {
	Register.Service.MediaType.Init(qdp.FindQuiddityByOrgIDURN, "", protocol.Software_PreAlpha, 1604939795)
	Register.Service.MediaType.SetDetail(protocol.LanguageEnglish,
		"Register Quiddity",
		"",
		[]string{"Quiddity"})
	Register.Service.SetAuthorization(protocol.CRUDCreate, protocol.UserType_Org)
}

type register struct {
	service.Service
}

func (ser *register) Process(st protocol.Stream, req qdp.Service_Register_Request) (err protocol.Error) {
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
	err = storage.Save(&q)
	return
}

func (ser *register) validateRequest(req qdp.Service_Register_Request) (err protocol.Error) {
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
