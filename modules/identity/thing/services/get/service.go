/* For license and copyright information please see the LEGAL file in the code repository */

package get

import (
	"libgo/protocol"
	"libgo/service"
)

var Service ser

type ser struct {
	service.Service
}

// /api/user/get/
func (s *ser) Init() {
	s.MediaType.Init("", "", protocol.Software_PreAlpha, 1605026701)
	s.MediaType.SetDetail(protocol.LanguageEnglish,
		"Get Quiddity",
		"",
		"",
		"",
		"",
		[]string{"Quiddity"})
	s.SetAuthorization(protocol.CRUD_Read, protocol.UserType_All)
}
