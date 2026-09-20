/* For license and copyright information please see the LEGAL file in the code repository */

package product

import (
	"libgo/gui"
	"libgo/protocol"
	"./quiddity"

	"../../service/quiddity"
)

type Page struct {
	gui.Page

	dom      gui.DOM
	som      gui.SOM
	template gui.DOM
}

// CreateState build the page in the requested state or reuse old states with SafeToSilentClose()
func (p *Page) CreateState(url string) protocol.GUIPageState {}

func test(element) {
	var req quiddity.GetRequest{

	}
// 	var err = req.SetQuiddityID("1abdfhosdh")
// 	if err != nil {
// 		element.Warn(err)
// 	}

	err = quiddity.GetService.Do(&req)
}
