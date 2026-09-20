/* For license and copyright information please see the LEGAL file in the code repository */

package servefiles_s

import (
	"memar/computer/datatype"
	datatype_p "memar/computer/datatype/protocol"
	"memar/net/http"
	http_p "memar/net/http/protocol"
	net_p "memar/net/protocol"
	operation_p "memar/process/operation/protocol"
	ser "memar/process/service"
	error_p "memar/process/error/protocol"

	www "org/modules/computer/www/internal"
	user_p "org/modules/identity/user/protocol"
)

var Service service

type service struct {
	datatype.DataType
	ser.Service

	www www.Assets
}

//memar:impl memar/computer/language/object/protocol.LifeCycle
func (s *service) Init() (err error_p.Error) {
	err = s.DataType.Init("domain/http.wg.ietf.org; type=service; name=serve-www")
	if err != nil {
		return
	}

	err = s.www.Init()
	return
}
func (s *service) Reinit() (err error_p.Error) {
	err = s.www.Reinit()
	return
}
func (s *service) Deinit() (err error_p.Error) {
	err = s.www.Deinit()
	return
}

//memar:impl memar/datatype/protocol.DataType_Details
func (s *service) LifeCycle() datatype_p.LifeCycle      { return datatype_p.LifeCycle_PreAlpha }
func (s *service) ReferenceURI() string                 { return "" }
func (s *service) IssueDate() string                    { return "" } // 1587282740
func (s *service) ExpiryDate() string                   { return "" }
func (s *service) ExpireInFavorOf() datatype_p.DataType { return nil }

//memar:impl memar/protocol.Service
func (s *service) URI() string                        { return "" }
func (s *service) Priority() operation_p.Priority     { return operation_p.Priority_Unset }
func (s *service) Weight() operation_p.Weight         { return operation_p.Weight_Unset }
func (s *service) ActionType() operation_p.ActionType { return operation_p.ActionType_All }
func (s *service) UserType() user_p.Type              { return user_p.Type_All }

// ServeWWW will serve WWW assets to request
func (s *service) ServeHTTP(sk net_p.Socket, httpReq http_p.Request, httpRes http_p.Response) (err error_p.Error) {
	var reqFile, _ = s.www.GUI.FileByPath(httpReq.Path())
	if reqFile == nil {
		// TODO::: SSR to serve-to-robots
		// TODO::: Have default error pages and can get customizes!
		// Send beauty HTML response in http error situation like 500, 404, ...

		const supportedLang = "en" // TODO::: get from header
		reqFile, err = s.www.MainHTMLDir.File(supportedLang)
		// if err != nil {
		// TODO::: check other user language and at the end send better error
		// }
	}
	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.Header_Set(http.HeaderKey_CacheControl, "max-age=31536000, immutable")
	httpRes.SetBody(reqFile.Data())
	return
}
