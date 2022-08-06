/* For license and copyright information please see LEGAL file in repository */

package storage

import (
	"github.com/GeniusesGroup/libgo/mediatype"
	"github.com/GeniusesGroup/libgo/protocol"
)

var MediaType mediatype.MediaType

func init() {
	// maintype "/" [tree "."] subtype ["+" suffix]* [";" parameters]
	MediaType.Init("domain/dp.protocol.storage+syllab; name=quiddity")
	MediaType.SetInfo(protocol.Software_PreAlpha, 1599455751, "")
	MediaType.SetDetail(protocol.LanguageEnglish, "Quiddity",
		`Quiddity is the essence of an object and with name or title of it in human languages and recently in machine languages`,
		"",
		"",
		"",
		[]string{})
	MediaType.SetDetail(protocol.LanguagePersian, "ماهیت",
		`ماهیت یعنی ذات و چیستی یک شئ که دارای نام یا عنوان مشخص در زبان های انسانی و جدیدا در زبان های ماشین می باشد`,
		"",
		"",
		"",
		[]string{})

	protocol.OS.RegisterMediaType(&MediaType)
}
