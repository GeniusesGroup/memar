/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"memar/protocol"
	"memar/service"
)

var getStreamsIDsService = service.Service{
	URN:                "domain/achaemenid.protocol.service; name=get-streams-ids",
	Domain:             DomainName,
	ID:                 16360337464082461731,
	IssueDate:          1595478242,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserTypeOwner,
	},

	Detail: map[protocol.LanguageID]service.ServiceDetail{
		protocol.LanguageEnglish: {
			Name:        "Get Streams IDs",
			Description: `Use by peer can get knowledge about all active StreamID on other party that use to close streams due to Due MaxConcurrentStreams.`,
			TAGS:        []string{},
		},
	},

	SRPCHandler: GetStreamsIDs,
}

// GetStreamsIDs use by peer can get knowledge about all active StreamID on other party that use to close streams due to Due MaxConcurrentStreams.
func GetStreamsIDs(st protocol.Stream) {
}

type getStreamsIDsReq struct {
}
