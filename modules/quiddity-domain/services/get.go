/* For license and copyright information please see LEGAL file in repository */

package services

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/service"

	"github.com/GeniusesGroup/organization/modules/quiddity-domain/internal/storage"
	qdp "github.com/GeniusesGroup/organization/modules/quiddity-domain/protocol"
)

var Get get
// /api/user/get/
func init() {
	Get.Service.MediaType.Init("", "", protocol.Software_PreAlpha, 1605026701)
	Get.Service.MediaType.SetDetail(protocol.LanguageEnglish,
		"Get Quiddity",
		"",
		"",
		"",
		[]string{"Quiddity"})
	Get.Service.SetAuthorization(protocol.CRUDRead, protocol.UserType_All)
}

type get struct {
	service.Service
}

func (ser *get) Process(st protocol.Stream, req qdp.Service_Get_Request) (res qdp.Service_Get_Response, err protocol.Error) {
	// TODO::: authorization??
	res, err = storage.Storage.Get(req.QuiddityID())
	return
}

func (ser *get) validateRequest(req qdp.Service_Get_Request) (err protocol.Error) {
	// TODO::: auto generate
	return
}
