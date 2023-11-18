/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"memar/protocol"
	"memar/service"
)

var syncTimeService = service.Service{
	URN:                "domain/achaemenid.protocol.service; name=sync-time",
	Domain:             DomainName,
	ID:                 4596775759005596018,
	IssueDate:          1595478242,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All,
	},

	Detail: map[protocol.LanguageID]service.ServiceDetail{
		protocol.LanguageEnglish: {
			Name:        "Sync Time",
			Description: `use to sync time between peer!`,
			TAGS:        []string{},
		},
	},

	SRPCHandler: SyncTime,
}

// SyncTime use to sync time between peer!
// https://en.wikipedia.org/wiki/Network_Time_Protocol
func SyncTime(st protocol.Stream) {
	// If the payload is not empty, the recipient MUST generate a PONG frame containing the same Data.
}

type syncTimeReq struct {
}
