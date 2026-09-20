/* For license and copyright information please see the LEGAL file in the code repository */

package quiddity

import (
	"libgo/mediatype"
	"libgo/protocol"
	"libgo/time/utc"

	org "../../protocol"
)

// maintype "/" [tree "."] subtype ["+" suffix]* [";" parameters]
// domain/sabz.city.storage+json; name=quiddity
var QuiddityMediaType = mediatype.New("domain/sabz.city.storage+syllab; name=quiddity").
	SetInfo(protocol.Software_PreAlpha, 1599455751, "").
	SetDetail(protocol.LanguageEnglish, "Quiddity",
		`Quiddity is the essence of an object and with name or title of it in human languages and recently in machine languages`,
		"",
		"",
		"",
		[]string{}).
	SetDetail(protocol.LanguagePersian, "ماهیت",
		`ماهیت یعنی ذات و چیستی یک شئ که دارای نام یا عنوان مشخص در زبان های انسانی و جدیدا در زبان های ماشین می باشد`,
		"",
		"",
		"",
		[]string{}).
	Expired(0, nil)

// Quiddity ---Read locale description in quiddityStructure---
type Quiddity struct {
	ID        [16]byte // Unique content ID in all languages!
	OrgID     [16]byte
	Language  protocol.Language
	URI       string // Locale name in the Computer world!!	https://en.quidditypedia.org/quiddity/Uniform_Resource_Identifier && https://en.quidditypedia.org/quiddity/Uniform_Resource_Name && https://en.quidditypedia.org/quiddity/Electronic_Product_Code
	Title     string // Locale name in the Human world!!		It can be not unique in all quiddity content.
	Status    org.Quiddity_Status
	time      utc.Time
	requestID [16]byte // user-request domain
}

func (q *Quiddity) QuiddityID() [16]byte       {}
func (q *Quiddity) DomainID() uint64           {}
func (q *Quiddity) Time() protocol.Time        { return &q.time }
func (q *Quiddity) RequestID() UserRequestUUID { return q.requestID }
